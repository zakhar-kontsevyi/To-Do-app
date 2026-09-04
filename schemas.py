from pydantic import BaseModel, Field , EmailStr 


class TaskAddSchema(BaseModel):
    title: str = Field(max_length=50)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    


class TaskSchema(TaskAddSchema):
    id: int



class UserAddSchema(BaseModel):
    username: str = Field(max_length=50)
    password: str 
    email: EmailStr

class UserSchema(UserAddSchema):
    id : int

class UserLoginSchema(BaseModel):
    username: str = Field(max_length=50)
    password: str = Field(max_length=64)