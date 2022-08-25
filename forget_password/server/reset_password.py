from fastapi import FastAPI
from server.model import models
from server.utilities import mail
from server.database import database
from fastapi.encoders import jsonable_encoder
from server.utilities import otp_generator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register")
async def register_user(data: dict):
    email = data["email"]
    password = data["password"]
    try:
        mail_details = await database.user_collection.find_one({"email": email})
        if mail_details == None:
            details = {
                "email": email,
                "password": password,
                "otp": 0,
                "verified": False
            }
            details: models.OtpValuation = models.OtpValuation(**details)
            details = jsonable_encoder(details)
            await database.user_collection.insert_one(details)
            return ("successfully registered")
        else:
            return ("email already existed")
    except Exception as e:
        return (str(e))


@app.post("/generate_otp")
async def generate_otp(data: dict):
    email = data["email"]
    try:
        mail_details = await database.user_collection.find_one({"email": email})
        if mail_details:
            otp = otp_generator.otp_generator()
            msg = mail.send_mail(email, otp[0])
            updated_student = await database.user_collection.update_one({"email": email}, {"$set": {"otp": int(otp[1]), "verified": False}})
        if updated_student:

            return ("otp generated")
        return False
    except Exception as e:
        return (str(e))


@app.post("/verify_otp")
async def verify_otp(data: dict):
    otp = data["otp"]
    email = data["email"]
    try:
        mail_details = await database.user_collection.find_one({"email": email})
        if int(otp) == mail_details["otp"]:
            await database.user_collection.update_one(
                {"email": email}, {"$set": {"verified": True}}
            )
            return ("otp verified successfully")
        else:
            await database.user_collection.update_one(
                {"email": email}, {"$set": {"verified": False}}
            )
            return ("wrong otp entered")
    except Exception as e:
        return (str(e))


@app.post("/change_password")
async def change_password(data: dict):
    email = data["email"]
    new_password = data["new_password"]
    try:
        mail_details = await database.user_collection.find_one({"email": email})
        if mail_details:
            if mail_details["verified"] == True:
                await database.user_collection.update_one(
                    {"email": email}, {"$set": {"password": new_password}}
                )
                await database.user_collection.update_one(
                    {"email": email}, {"$set": {"verified": False}}
                )
                return ("password changed successfully")
            else:
                return ("otp is not verified for this mail")
        else:
            return ("invalid mail")
    except Exception as e:
        return (str(e))
