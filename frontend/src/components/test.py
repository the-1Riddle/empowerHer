from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import os

load_dotenv('.env')

app = FastAPI()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_FROM'),
    MAIL_PORT=int(os.getenv('MAIL_PORT')),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_FROM_NAME=os.getenv('MAIL_FROM_NAME'),
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)

class EmailSchema(BaseModel):
    email: EmailStr
    full_name: str
    subject: str
    phone_number: str
    message: str

@app.post("/contact/")
async def contact(request: Request, email: EmailStr = Form(...), full_name: str = Form(...), subject: str = Form(...), phone_number: str = Form(...), message: str = Form(...)):
    email_data = EmailSchema(
        email=email,
        full_name=full_name,
        subject=subject,
        phone_number=phone_number,
        message=message
    )

    message = MessageSchema(
        subject=f"New Contact Form Submission: {email_data.subject}",
        recipients=[os.getenv('MAIL_USERNAME')],  # Your email address
        body=f"""
        Full Name: {email_data.full_name}
        Email: {email_data.email}
        Phone Number: {email_data.phone_number}
        Message: {email_data.message}
        """,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    
    return JSONResponse(status_code=200, content={"message": "Email has been sent"})

