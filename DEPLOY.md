# Hackathon Rivals — Deployment Guide

## Quick Deploy (5 minutes)

### Option 1: Netlify (Recommended)
1. Push this folder to GitHub
2. Connect repo to Netlify
3. Add environment variables in Netlify dashboard:
   - `VITE_SUPABASE_URL` = your Supabase project URL
   - `VITE_SUPABASE_ANON_KEY` = your Supabase anon key
   - `VITE_FORMSPREE_URL` = your Formspree endpoint (optional)
4. Deploy!

### Option 2: Vercel
1. Push to GitHub
2. Import in Vercel
3. Add same environment variables
3. Deploy!

### Option 3: Cloudflare Pages
1. Connect GitHub repo
2. Build command: `echo 'static'`
3. Output directory: `.`
4. Add env vars
5. Deploy!

## Supabase Setup

1. Create new project at supabase.com
2. Go to SQL Editor → Run `schema.sql`
3. Go to Authentication → Providers → Enable Email/Password
4. Go to Storage → Create bucket `team-ppts` (private)
5. Copy Project URL & Anon Key to deployment env vars

## Required Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_SUPABASE_URL` | Yes | `https://xxx.supabase.co` |
| `VITE_SUPABASE_ANON_KEY` | Yes | `sb_publishable_xxx` |
| `VITE_FORMSPREE_URL` | No | For contact form emails |

## PWA Icons
Open `generate-icons.html` in browser → Download both icons → Place in root folder

## Features Included
- ✅ Team registration (4-step wizard)
- ✅ Code Arena (39 languages, Judge0)
- ✅ Code Lab (live preview)
- ✅ Real-time leaderboard
- ✅ Admin dashboard (9 tabs)
- ✅ AI Mentor chat
- ✅ Announcements system
- ✅ Certificate generation
- ✅ Judge management
- ✅ Schedule management
- ✅ Results publishing
- ✅ PWA support

## Post-Deploy Checklist
- [ ] Run `schema.sql` in Supabase
- [ ] Create `team-ppts` storage bucket
- [ ] Set environment variables
- [ ] Test registration flow
- [ ] Test Code Arena
- [ ] Verify admin access (create first admin via Supabase dashboard)
- [ ] Configure webhook in Admin → Settings
- [ ] Test email notifications

## Admin Access
First admin must be created manually in Supabase:
```sql
-- In Supabase SQL Editor
insert into profiles (id, email, full_name, role)
values ('<auth-user-id>', 'admin@college.edu', 'Admin Name', 'Admin');
```

## Support
- Issues: GitHub Issues
- Email: hello@hackathonrivals.in