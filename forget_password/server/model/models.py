from pydantic import BaseModel, EmailStr

class OtpValuation(BaseModel):
    
    email: EmailStr
    password:str
    otp: int 
    verified:bool
# creating a schema.