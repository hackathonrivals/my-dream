-- Hackathon Rivals Season 2026 — Supabase Schema
-- Run this in Supabase SQL Editor

-- Enable required extensions
create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";

-- Profiles table (extends auth.users)
create table if not exists profiles (
  id uuid primary key references auth.users on delete cascade,
  email text not null,
  full_name text,
  role text not null default 'Student' check (role in ('Student','SPOC','Judge','Admin')),
  college text,
  designation text,
  organization text,
  expertise text,
  avatar_color text default '#7c5cff',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Team Registrations
create table if not exists team_registrations (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid not null references auth.users on delete cascade,
  email text not null,
  spoc_name text not null,
  spoc_designation text,
  spoc_email text not null,
  spoc_mobile text,
  college_name text not null,
  college_city text,
  college_address text,
  team_name text not null,
  team_size int not null default 1,
  theme text not null,
  category text not null check (category in ('Software','Hardware','Student Innovation')),
  problem_statement text,
  idea_summary text,
  members jsonb not null default '[]',
  status text not null default 'submitted' check (status in ('submitted','approved','rejected')),
  ppt_url text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Arena Submissions
create table if not exists arena_submissions (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references auth.users on delete set null,
  email text not null,
  full_name text,
  role text,
  title text not null,
  question text,
  code text,
  lang text not null,
  score int not null default 0,
  hint_count int not null default 0,
  penalty int not null default 0,
  topic text,
  tag text,
  breakdown jsonb,
  test_cases jsonb,
  source text not null default 'app' check (source in ('app','import')),
  flagged boolean not null default false,
  flag_reason text,
  flagged_at timestamptz,
  imported_by uuid references auth.users,
  created_at timestamptz default now()
);

-- Contact Messages
create table if not exists contact_messages (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  email text not null,
  phone text,
  org text,
  category text not null default 'General',
  subject text not null,
  message text not null,
  status text not null default 'new' check (status in ('new','read','replied','archived')),
  read_at timestamptz,
  replied_at timestamptz,
  created_at timestamptz default now()
);

-- Testimonials
create table if not exists testimonials (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  role text,
  quote text not null,
  rating int not null default 5 check (rating between 1 and 5),
  avatar_color text default '#7c5cff',
  display_order int not null default 0,
  published boolean not null default true,
  created_at timestamptz default now()
);

-- Announcements
create table if not exists announcements (
  id uuid primary key default uuid_generate_v4(),
  title text not null,
  body text not null,
  type text not null default 'general' check (type in ('general','deadline','result','maintenance','feature')),
  audience text not null default 'all' check (audience in ('all','students','spocs','judges','admins')),
  status text not null default 'draft' check (status in ('draft','scheduled','sent')),
  scheduled_for timestamptz,
  sent_at timestamptz,
  created_by uuid references auth.users,
  created_at timestamptz default now()
);

-- Certificates
create table if not exists certificates (
  id uuid primary key default uuid_generate_v4(),
  participant_name text not null,
  participant_email text not null,
  type text not null check (type in ('participation','winner','runner-up','special')),
  team_name text,
  rank int,
  track text,
  score int,
  certificate_url text,
  generated_at timestamptz default now(),
  generated_by uuid references auth.users
);

-- Judges
create table if not exists judges (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  email text not null unique,
  expertise text,
  organization text,
  assigned_ps text[],
  status text not null default 'invited' check (status in ('invited','accepted','declined','completed')),
  reviews_done int not null default 0,
  invite_code text,
  invited_at timestamptz default now(),
  accepted_at timestamptz,
  created_by uuid references auth.users
);

-- Schedule
create table if not exists schedule (
  id uuid primary key default uuid_generate_v4(),
  title text not null,
  description text,
  event_date timestamptz not null,
  duration text,
  location text,
  type text not null default 'general' check (type in ('general','workshop','ceremony','deadline','judging')),
  status text not null default 'upcoming' check (status in ('upcoming','live','completed','cancelled')),
  created_by uuid references auth.users,
  created_at timestamptz default now()
);

-- Results
create table if not exists results (
  id uuid primary key default uuid_generate_v4(),
  team_name text not null,
  college_name text,
  track text not null,
  rank int,
  score int not null default 0,
  prize text,
  submission_id uuid references arena_submissions,
  published boolean not null default false,
  published_at timestamptz,
  created_at timestamptz default now()
);

-- App Settings (for webhook URLs, etc.)
create table if not exists app_settings (
  key text primary key,
  value text,
  updated_at timestamptz default now()
);

-- Import Log
create table if not exists arena_import_log (
  id uuid primary key default uuid_generate_v4(),
  admin_id uuid references auth.users,
  admin_email text,
  row_count int not null default 0,
  failed_count int not null default 0,
  file_name text,
  created_at timestamptz default now()
);

-- Row Level Security
alter table profiles enable row level security;
alter table team_registrations enable row level security;
alter table arena_submissions enable row level security;
alter table contact_messages enable row level security;
alter table testimonials enable row level security;
alter table announcements enable row level security;
alter table certificates enable row level security;
alter table judges enable row level security;
alter table schedule enable row level security;
alter table results enable row level security;
alter table app_settings enable row level security;
alter table arena_import_log enable row level security;

-- Policies
create policy "Users can view own profile" on profiles for select using (auth.uid() = id);
create policy "Users can update own profile" on profiles for update using (auth.uid() = id);
create policy "Admins can view all profiles" on profiles for select using (
  exists (select 1 from profiles where id = auth.uid() and role = 'Admin')
);

create policy "Users can view own registrations" on team_registrations for select using (auth.uid() = user_id);
create policy "Users can insert own registrations" on team_registrations for insert with check (auth.uid() = user_id);
create policy "Admins can manage all registrations" on team_registrations for all using (
  exists (select 1 from profiles where id = auth.uid() and role = 'Admin')
);

create policy "Users can view own submissions" on arena_submissions for select using (auth.uid() = user_id);
create policy "Users can insert own submissions" on arena_submissions for insert with check (auth.uid() = user_id);
create policy "Admins can manage all submissions" on arena_submissions for all using (
  exists (select 1 from profiles where id = auth.uid() and role = 'Admin')
);

create policy "Anyone can insert contact messages" on contact_messages for insert with check (true);
create policy "Admins can manage messages" on contact_messages for all using (
  exists (select 1 from profiles where id = auth.uid() and role = 'Admin')
);

create policy "Published testimonials visible to all" on testimonials for select using (published = true);
create policy "Admins manage testimonials" on testimonials for all using (
  exists (select 1 from profiles where id = auth.uid() and role = 'Admin')
);

create policy "Announcements visible by audience" on announcements for select using (
  status = 'sent' and (audience = 'all' or 
    (audience = 'students' and exists (select 1 from profiles where id = auth.uid() and role = 'Student')) or
    (audience = 'spocs' and exists (select 1 from profiles where id = auth.uid() and role = 'SPOC')) or
    (audience = 'judges' and exists (select 1 from profiles where id = auth.uid() and role = 'Judge')) or
    (audience = 'admins' and exists (select 1 from profiles where id = auth.uid() and role = 'Admin')))
);
create policy "Admins manage announcements" on announcements for all using (
  exists (select 1 from profiles where id = auth.uid() and role = 'Admin')
);

create policy "Users can view own certificates" on certificates for select using (participant_email = (select email from profiles where id = auth.uid()));
create policy "Admins manage certificates" on certificates for all using (
  exists (select 1 from profiles where id = auth.uid() and role = 'Admin')
);

create policy "Judges view own" on judges for select using (email = (select email from profiles where id = auth.uid()));
create policy "Admins manage judges" on judges for all using (
  exists (select 1 from profiles where id = auth.uid() and role = 'Admin')
);

create policy "Schedule visible to all" on schedule for select using (true);
create policy "Admins manage schedule" on schedule for all using (
  exists (select 1 from profiles where id = auth.uid() and role = 'Admin')
);

create policy "Published results visible" on results for select using (published = true);
create policy "Admins manage results" on results for all using (
  exists (select 1 from profiles where id = auth.uid() and role = 'Admin')
);

create policy "Admins manage settings" on app_settings for all using (
  exists (select 1 from profiles where id = auth.uid() and role = 'Admin')
);

create policy "Admins view import log" on arena_import_log for select using (
  exists (select 1 from profiles where id = auth.uid() and role = 'Admin')
);
create policy "Admins insert import log" on arena_import_log for insert with check (
  exists (select 1 from profiles where id = auth.uid() and role = 'Admin')
);

-- Storage bucket for PPT uploads
insert into storage.buckets (id, name, public) values ('team-ppts', 'team-ppts', false) on conflict do nothing;
create policy "Users upload own PPT" on storage.objects for insert with check (bucket_id = 'team-ppts' and auth.uid()::text = (storage.foldername(name))[1]);
create policy "Users view own PPT" on storage.objects for select using (bucket_id = 'team-ppts' and auth.uid()::text = (storage.foldername(name))[1]);
create policy "Admins manage all PPTs" on storage.objects for all using (
  exists (select 1 from profiles where id = auth.uid() and role = 'Admin')
);

-- Indexes for performance
create index if not exists idx_team_reg_user on team_registrations(user_id);
create index if not exists idx_team_reg_status on team_registrations(status);
create index if not exists idx_arena_user on arena_submissions(user_id);
create index if not exists idx_arena_created on arena_submissions(created_at desc);
create index if not exists idx_arena_flagged on arena_submissions(flagged) where flagged = true;
create index if not exists idx_contact_status on contact_messages(status);
create index if not exists idx_ann_status on announcements(status);
create index if not exists idx_results_track_rank on results(track, rank);