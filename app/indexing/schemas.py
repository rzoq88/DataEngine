import uuid
import json
from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional


class DataIndexSchema(BaseModel):
    objectID: str = Field(alias='item_id')
    objectType: str = "Data"
    email: Optional[str]
    title: Optional[str]
    password :Optional[str] 
    url :Optional[str] 
    firstname :Optional[str] 
    lastname :Optional[str] 
    address :Optional[str] 
    ip :Optional[str] 
    hashpassword :Optional[str] 
    dateofbirth :Optional[str] 
    gender :Optional[str] 
    username :Optional[str] 
    path: str = Field(alias='item_id')
        
    @validator("path")
    def set_path(cls, v, values, **kwargs):
        item_id = v
        return f"/data/{item_id}"


