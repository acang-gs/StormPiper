from typing import Optional

from .base import BaseModel, BaseORM


# Shared properties
class TMNTFacilityAttrBase(BaseModel):

    # modeling attrs
    facility_type: Optional[str] = None
    hsg: Optional[str] = None
    design_storm_depth_inches: Optional[float] = None
    tributary_area_tc_min: Optional[float] = None
    total_volume_cuft: Optional[float] = None
    area_sqft: Optional[float] = None
    inf_rate_inhr: Optional[float] = None
    retention_volume_cuft: Optional[float] = None
    media_filtration_rate_inhr: Optional[float] = None
    minimum_retention_pct_override: Optional[float] = None
    treatment_rate_cfs: Optional[float] = None
    depth_ft: Optional[float] = None

    # simplified attrs
    captured_pct: Optional[float] = None
    retained_pct: Optional[float] = None

    # cost attrs
    capital_cost: Optional[float] = None
    om_cost_per_yr: Optional[float] = None
    lifespan_yrs: Optional[float] = None
    replacement_cost: Optional[float] = None


# Properties to receive on creation
class TMNTFacilityAttrCreate(TMNTFacilityAttrBase):
    pass


# Properties to receive on update
class TMNTFacilityAttrPatch(TMNTFacilityAttrBase):
    pass


# Properties to send on update
class TMNTFacilityAttrUpdate(TMNTFacilityAttrPatch):
    updated_by: Optional[str] = None
    net_present_value: Optional[float] = None


# Properties shared by models stored in DB
class TMNTFacilityAttrInDBBase(BaseORM, TMNTFacilityAttrBase):
    altid: str

    basinname: Optional[str] = None
    subbasin: Optional[str] = None
    net_present_value: Optional[float] = None


# Properties to return to client
class TMNTFacilityAttr(TMNTFacilityAttrInDBBase):
    pass


# Properties properties stored in DB
class TMNTFacilityAttrInDB(TMNTFacilityAttrInDBBase):
    pass
