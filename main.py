import os
import smtplib
from email.mime.text import MIMEText

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client

app = FastAPI()

# Allow requests from your portfolio site
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can lock this to ["https://ayesha-cs-93.github.io"] later
    allow_methods=["POST"],
    allow_headers=["*"],
)

# ---- Config (set these as environment variables on your host, never hardcode secrets) ----
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
GMAIL_ADDRESS = os.environ["GMAIL_ADDRESS"]        # the gmail you send FROM
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]  # 16-char Gmail App Password
NOTIFY_EMAIL = os.environ.get("NOTIFY_EMAIL", GMAIL_ADDRESS)  # where you receive notifications

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str


def send_email_notification(name: str, email: str, message: str):
    body = f"New portfolio contact form submission:\n\nName: {name}\nEmail: {email}\nMessage:\n{message}"
    msg = MIMEText(body)
    msg["Subject"] = "New portfolio contact submission"
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = NOTIFY_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.send_message(msg)


@app.post("/contact")
def submit_contact(form: ContactForm):
    # 1. Save to Supabase
    try:
        supabase.table("contact_submissions").insert({
            "name": form.name,
            "email": form.email,
            "message": form.message,
        }).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    # 2. Send email notification (non-fatal if it fails)
    try:
        send_email_notification(form.name, form.email, form.message)
    except Exception as e:
        print(f"Email failed but submission was saved: {e}")

    return {"status": "ok", "message": "Thanks! Your message was received."}


@app.get("/")
def health_check():
    return {"status": "alive"}
