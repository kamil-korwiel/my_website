from datetime import datetime
from sqlmodel import Field, SQLModel


class Blog(SQLModel, table=True):
    id: str = Field(primary_key=True)
    title: str
    date: datetime
    file_md_path: str
    
    # @field_serializer("date")
    # def serialize_date(self, value: datetime) -> str:
    #     return value.strftime("%d.%m.%Y")
    
    # @field_validator('id', mode='before')
    # @classmethod
    # def validate_id(cls, value:str) -> str:
    #     if isinstance(value, str):
    #         if not value.find(" "):
    #             print("HIT")
    #             return value.lower()
    #         else:
    #             ValueError("ID need not to contains white spaces")
    #     else:
    #         ValueError("ID is not String")
    
