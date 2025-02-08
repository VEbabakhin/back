from pydantic import BaseModel, Field


class HotelPATCH(BaseModel):
    title: str = Field(None)
    name: str = Field(None)


class Hotel(BaseModel):
    title: str
    name: str