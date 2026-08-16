# Contact Form Backend — Setup Steps

## What this is
A FastAPI backend with one endpoint (`/contact`) that:
1. Receives your portfolio's contact form data
2. Saves it to a Supabase table
3. Emails you a notification via Gmail

## Step 1 — Supabase table
1. Go to supabase.com, open your project (or create a free one).
2. Go to SQL Editor → New query → paste the contents of `supabase_setup.sql` → Run.
3. Go to Project Settings → API. Copy:
   - `Project URL` → this is your `SUPABASE_URL`
   - `anon public` key → this is your `SUPABASE_KEY`

## Step 2 — Gmail App Password (so the backend can send you email)
1. Go to your Google Account → Security → 2-Step Verification (must be ON).
2. Go to Security → App passwords.
3. Create a new app password (name it "portfolio-backend"). Copy the 16-character password.
   This is your `GMAIL_APP_PASSWORD`. Your `GMAIL_ADDRESS` is your normal Gmail address.

## Step 3 — Push this code to GitHub
1. Create a new repo, e.g. `github.com/ayesha-cs-93/contact-form-backend`
2. Push these 3 files: `main.py`, `requirements.txt`, and this README (skip the sql/html files, they're just for reference).

## Step 4 — Deploy free on Render
1. Go to render.com → sign up with GitHub (free).
2. New → Web Service → connect your `contact-form-backend` repo.
3. Settings:
   - Runtime: Python 3
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Instance type: Free
4. Under "Environment", add these environment variables:
   - `SUPABASE_URL` = (from Step 1)
   - `SUPABASE_KEY` = (from Step 1)
   - `GMAIL_ADDRESS` = your gmail address
   - `GMAIL_APP_PASSWORD` = (from Step 2)
   - `NOTIFY_EMAIL` = ayesha.farooq.cs93@gmail.com
5. Click "Create Web Service". Wait for it to deploy (~2-3 min).
6. Once live, you'll get a URL like `https://contact-form-backend-xxxx.onrender.com`
   Test it by visiting that URL in a browser — you should see `{"status":"alive"}`.

## Step 5 — Connect your portfolio
1. Open `frontend-snippet.html`, replace `YOUR-BACKEND-URL` with your real Render URL.
2. Add the contact section + nav button into your `index.html` (see comments in the file).
3. Push to GitHub, wait ~1 min for GitHub Pages to rebuild.
4. Fill out the form on your live site and check: (a) a row appears in Supabase's Table Editor,
   and (b) you get an email.

## Note on Render free tier
Free web services on Render "sleep" after inactivity — the first request after sleeping can take
10-20 seconds to respond. This is normal and fine for this assignment.
