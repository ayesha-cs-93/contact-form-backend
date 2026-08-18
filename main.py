import os
import resend

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

# ---- Config (set these as environment variables on Railway, never hardcode secrets) ----
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
resend.api_key = os.environ["RESEND_API_KEY"]
NOTIFY_EMAIL = os.environ.get("NOTIFY_EMAIL", "ayesha.farooq.cs93@gmail.com")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str


def send_email_notification(name: str, email: str, message: str):
    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": NOTIFY_EMAIL,
        "subject": "New portfolio contact submission",
        "text": f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
    })


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
