from pydantic import BaseModel, Field, EmailStr


class BaseUserInfo(BaseModel):
    name: str = Field(max_length=100, min_length=1, examples=['Тарас'], description='Name of the new user')
    surname: str = Field(max_length=100, min_length=1, examples=['Мельник'], description='Surname of the new user')
    email: EmailStr = Field(examples=['test_hillel_api_mailing@ukr.net'], description='EMAIL of the user')


class UserPasswordField(BaseModel):
    password: str = Field(description='your password', examples=['12345678'], min_length=8)


class RegisterUserRequest(BaseUserInfo, UserPasswordField):
    pass
