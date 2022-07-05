import logging
from typing import List, Optional

import geopandas
import pandas
import sqlalchemy as sa
from geoalchemy2.shape import to_shape
from sqlalchemy.event import listen
from tenacity import after_log  # type: ignore
from tenacity import before_log  # type: ignore
from tenacity import stop_after_attempt  # type: ignore
from tenacity import wait_fixed  # type: ignore
from tenacity import retry

from stormpiper.core.utils import datetime_to_isoformat

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def orm_to_dict(row) -> dict:
    """Convert an ORM return object to a dict."""
    row_dict = {col: getattr(row, col) for col in row.__table__.columns.keys()}
    return row_dict


def scalars_to_records(rows) -> List[dict]:
    """Convert ORM scalars to list of dicts [records]"""

    return [orm_to_dict(row) for row in rows]


def scalar_records_to_gdf(
    records: List[dict], crs: Optional[int] = None, geometry: str = "geom"
) -> geopandas.GeoDataFrame:
    if crs is None:
        crs = 4326
    data = (
        pandas.DataFrame(records)
        .assign(geometry=lambda df: df[geometry].apply(lambda x: to_shape(x)))
        .pipe(datetime_to_isoformat)
    )
    gdf = geopandas.GeoDataFrame(data, geometry="geometry", crs=crs)  # type: ignore

    if geometry != "geometry":
        gdf.drop(columns=[geometry], inplace=True)
    return gdf


def scalars_to_gdf(
    scalars: List, crs: Optional[int] = None, geometry: str = "geom"
) -> geopandas.GeoDataFrame:
    records = scalars_to_records(scalars)
    return scalar_records_to_gdf(records, crs=crs, geometry=geometry)


def delete_and_replace_postgis_table(
    *, gdf: geopandas.GeoDataFrame, table_name: str, engine, **kwargs
) -> None:
    """
    Overwrites contents of `table_name` with contents of gdf.
    gdf schema must match destination table if the table already exists.
    """
    with engine.begin() as conn:
        if engine.dialect.has_table(conn, table_name):
            conn.execute(f"delete from {table_name}")
        gdf = gdf.rename_geometry("geom")  # type: ignore
        return gdf.to_postgis(table_name, con=conn, if_exists="append", **kwargs)


def delete_and_replace_table(
    *, df: pandas.DataFrame, table_name: str, engine, **kwargs
) -> None:
    """
    Overwrites contents of `table_name` with contents of df.
    df schema must match destination table if the table already exists.
    """
    with engine.begin() as conn:
        if engine.dialect.has_table(conn, table_name):
            conn.execute(f"delete from {table_name}")
        return df.to_sql(table_name, con=conn, if_exists="append", **kwargs)


@retry(
    stop=stop_after_attempt(60 * 5),  # 5 mins
    wait=wait_fixed(2),  # 2 seconds
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def reconnect_engine(engine):
    try:
        with engine.begin() as conn:
            # this should connect/login and ensure that the database is available.
            conn.execute("select 1").fetchall()

    except Exception as e:
        logger.error(e)
        logger.info("Engine connection url:", engine.url)
        raise e


def load_spatialite_extension(conn, connection_record):
    conn.enable_load_extension(True)
    conn.load_extension("mod_spatialite")


def load_spatialite(engine):
    listen(engine, "connect", load_spatialite_extension)
    with engine.begin() as conn:
        conn.execute(sa.select([sa.func.InitSpatialMetaData()]))


def init_spatial(engine):
    inspector = sa.inspect(engine)
    if "spatial_ref_sys" in inspector.get_table_names():
        logger.info("spatial plugins already enabled.")
        return

    if "sqlite" in engine.url:
        logger.info("enabling spatialite...")
        load_spatialite(engine)
        logger.info("enabling spatialite...complete.")
        return

    logger.error("postgis or libspatialite required.")
