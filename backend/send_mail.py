#!/usr/bin/python3
"""
This file contains the code to send emails using FastAPI and FastMail
"""
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

EmailSchema = __import__("schemas").EmailSchema


load_dotenv('.env')

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_FROM'),
    MAIL_PORT=int(os.getenv('MAIL_PORT')),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_FROM_NAME=os.getenv('MAIL_FROM_NAME'),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

# Function to send contact email
async def contact(email_data: EmailSchema):
    message = MessageSchema(
        subject=f"New Contact Form Submission: {email_data.subject}",
        recipients=[os.getenv('MAIL_USERNAME')],
        body=f"""
        Full Name: {email_data.full_name}<br>
        Email: {email_data.email}<br>
        Phone Number: {email_data.phone_number}<br>
        Message: {email_data.message}
        """,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
