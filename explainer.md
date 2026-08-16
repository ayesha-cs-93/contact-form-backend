# Plain-Words Explainer — Contact Form Feature

**What a backend is:**
A backend is the part of an app that runs on a server, not in the visitor's browser. It receives
data, processes it, talks to a database, and sends back a response. The visitor never sees this
code directly — they only see the result.

**What my feature does:**
My portfolio now has a working contact form. A visitor can type their name, email, and a message,
and hit send. That data doesn't just disappear — it gets saved somewhere I can actually read it,
and I get notified by email the moment someone submits it.

**How the data flows:**
1. The visitor fills the form and clicks Send.
2. My portfolio's JavaScript packages that data and sends it as a request to my FastAPI backend
   (hosted on Render).
3. The backend validates the data (checks the email is a real email format, no fields are empty).
4. The backend inserts the data as a new row into a Supabase (PostgreSQL) database table.
5. The backend also sends me an email via Gmail with the submission details.
6. The backend sends a success response back to the browser, which shows the visitor a
   "Thanks, your message was received" message.

The visitor's browser never touches the database or my email directly — it only ever talks to
my backend, and my backend is the only thing with permission to write to the database and send
the email. That separation is the whole point of having a backend.
