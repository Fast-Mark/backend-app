from typing import List

from pydantic import BaseModel, Field, validator

class Element(BaseModel):
    key: str | None 
    poistion_x: int | None = 0
    position_y: int | None = 0
    font_family: str | None = "Arial"
    font_size:  int | None = 18
    font_color: str | None = "#000000"
    # TODO: сделать константы как во фронте
    font_style: str | None =  "basic"
    aligment: str = Field()

    # @validator('alignment')
    # def validate_alignment(cls, value):
    #     allowed_values = {'left', 'right', 'center'}
    #     if value not in allowed_values:
    #         raise ValueError(f'alignment must be one of {allowed_values}, not {value}')
    #     return value

class ElementsList(BaseModel):
    elements: List[Element]



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str