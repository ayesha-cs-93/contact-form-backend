-- Run this in Supabase: Project -> SQL Editor -> New Query -> paste -> Run

create table contact_submissions (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  email text not null,
  message text not null,
  created_at timestamp with time zone default now()
);
