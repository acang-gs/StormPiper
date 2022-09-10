"""add src ctrl load reduction tables

Revision ID: 5609bfd21d8d
Revises: 175b76dedf85
Create Date: 2022-08-29 18:55:16.478649

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5609bfd21d8d"
down_revision = "175b76dedf85"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "lgu_load_to_structural",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("node_id", sa.String(), nullable=True),
        sa.Column("epoch", sa.String(), nullable=True),
        sa.Column("variable", sa.String(), nullable=True),
        sa.Column("value", sa.Float(), nullable=True),
        sa.Column("units", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tmnt_source_control_downstream_load_reduced",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("node_id", sa.String(), nullable=False),
        sa.Column("subbasin", sa.String(), nullable=False),
        sa.Column("basinname", sa.String(), nullable=True),
        sa.Column("variable", sa.String(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=True),
        sa.Column("activity", sa.String(), nullable=False),
        sa.Column(
            "direction",
            postgresql.ENUM(name="direction", create_type=False),
            nullable=False,
        ),
        sa.Column("epoch", sa.String(), nullable=True),
        sa.Column("value", sa.Float(), nullable=True),
        sa.Column("units", sa.String(), nullable=True),
        sa.Column("percent_reduction", sa.Float(), nullable=True),
        sa.Column("value_remaining_prev", sa.Float(), nullable=True),
        sa.Column("value_remaining", sa.Float(), nullable=True),
        sa.Column("load_reduced", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tmnt_source_control_upstream_load_reduced",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("node_id", sa.String(), nullable=False),
        sa.Column("subbasin", sa.String(), nullable=False),
        sa.Column("basinname", sa.String(), nullable=True),
        sa.Column("variable", sa.String(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=True),
        sa.Column("activity", sa.String(), nullable=False),
        sa.Column(
            "direction",
            postgresql.ENUM(name="direction", create_type=False),
            nullable=False,
        ),
        sa.Column("epoch", sa.String(), nullable=True),
        sa.Column("value", sa.Float(), nullable=True),
        sa.Column("units", sa.String(), nullable=True),
        sa.Column("percent_reduction", sa.Float(), nullable=True),
        sa.Column("value_remaining_prev", sa.Float(), nullable=True),
        sa.Column("value_remaining", sa.Float(), nullable=True),
        sa.Column("load_reduced", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "load_to_ds_src_ctrl",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("node_id", sa.String(), nullable=True),
        sa.Column("epoch", sa.String(), nullable=True),
        sa.Column("variable", sa.String(), nullable=True),
        sa.Column("value", sa.Float(), nullable=True),
        sa.Column("units", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.alter_column(
        "tmnt_source_control", "pollutant", nullable=False, new_column_name="variable"
    )
    op.drop_constraint(
        "tmnt_source_control_direction_subbasin_pollutant_activity_key",
        "tmnt_source_control",
        type_="unique",
    )
    op.drop_constraint(
        "tmnt_source_control_direction_subbasin_pollutant_order_key",
        "tmnt_source_control",
        type_="unique",
    )
    op.create_unique_constraint(
        None,
        "tmnt_source_control",
        ["direction", "subbasin", "variable", "activity"],
    )
    op.create_unique_constraint(
        None,
        "tmnt_source_control",
        ["direction", "subbasin", "variable", "order"],
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "tmnt_source_control", "variable", nullable=False, new_column_name="pollutant"
    )
    op.drop_constraint(
        "tmnt_source_control_direction_subbasin_variable_activity_key",
        "tmnt_source_control",
        type_="unique",
    )
    op.drop_constraint(
        "tmnt_source_control_direction_subbasin_variable_order_key",
        "tmnt_source_control",
        type_="unique",
    )
    op.create_unique_constraint(
        "tmnt_source_control_direction_subbasin_pollutant_order_key",
        "tmnt_source_control",
        ["direction", "subbasin", "pollutant", "order"],
    )
    op.create_unique_constraint(
        "tmnt_source_control_direction_subbasin_pollutant_activity_key",
        "tmnt_source_control",
        ["direction", "subbasin", "pollutant", "activity"],
    )

    op.drop_table("tmnt_source_control_upstream_load_reduced")
    op.drop_table("tmnt_source_control_downstream_load_reduced")
    op.drop_table("lgu_load_to_structural")
    op.drop_table("load_to_ds_src_ctrl")
    # ### end Alembic commands ###
