from pydantic import BaseModel, Field


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


class UserUpdatePhoneNumber(BaseModel):
    password: str
    new_phone_number: str = Field(max_length=11, min_length=11, pattern=r"^\d+$")
