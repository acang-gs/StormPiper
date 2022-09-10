from typing import Optional

from stormpiper.database.schemas.tmnt import Direction

from .base import BaseModel


# Shared properties
class TMNTSourceControlBase(BaseModel):

    activity: Optional[str] = None
    subbasin: Optional[str] = None
    direction: Optional[Direction] = None

    # if multiple for same subbasin, variable, and direction, will be applied in order
    # least to greatest default is last.
    order: Optional[int] = None

    # this is the pollutant acted upon. entered as an upper case abbreviation.
    variable: Optional[str] = None

    # must be float between 0.0 and 100.0
    percent_reduction: Optional[float] = None


# Properties to recieve on creation
class TMNTSourceControlPost(TMNTSourceControlBase):
    pass


# Properties to send on creation
class TMNTSourceControlCreate(TMNTSourceControlPost):
    updated_by: Optional[str] = None


# Properties to receive on update
class TMNTSourceControlPatch(TMNTSourceControlBase):
    pass


# Properties to send on update
class TMNTSourceControlUpdate(TMNTSourceControlPatch):
    updated_by: Optional[str] = None


# Properties shared by models stored in DB
class TMNTSourceControlInDBBase(TMNTSourceControlBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class TMNTSourceControl(TMNTSourceControlInDBBase):
    pass


# properties stored in DB
# class TMNTFacilityAttrInDB(TMNTFacilityAttrInDBBase):
#     pass
