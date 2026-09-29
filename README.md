# Hackathon Rivals — Season 2026

India's National Hackathon Arena for Student Innovators

## Features
- 🏗️ **Team Registration** — 4-step wizard with SPOC, team, members, idea submission
- ⚔️ **Code Arena** — 39 languages, Judge0 CE, test cases, hints, scoring
- 💻 **Code Lab** — Live HTML/React preview, instant execution
- 🏆 **Real-time Leaderboard** — Live, weekly, monthly, by submissions
- 🤖 **AI Mentor** — Contextual help for themes, PS, judging, strategy
- 🛡️ **Admin Dashboard** — 9 tabs: submissions, teams, testimonials, messages, announcements, certificates, judges, schedule, results
- 📢 **Announcements** — Draft/scheduled/sent, audience targeting
- 🏅 **Certificates** — Generate, bulk create, download, email
- ⚖️ **Judge Panel** — Invite, expertise, review tracking
- 📅 **Schedule** — Event calendar with status
- 🏁 **Results** — Track winners, overall champions, special awards
- 📱 **PWA** — Installable, offline-ready

## Tech Stack
- Single HTML file (no build step)
- Supabase (Auth, Database, Storage, Realtime)
- Judge0 CE (Code execution)
- Formspree (Contact emails)
- Vanilla JS (ES6+)

## Quick Start
```bash
# Deploy to Netlify/Vercel/Cloudflare Pages
# 1. Push to GitHub
# 2. Connect repo
# 3. Add env vars (see DEPLOY.md)
# 4. Deploy
```

## Environment Variables
```
VITE_SUPABASE_URL=https://xxx.supabase.co
VITE_SUPABASE_ANON_KEY=sb_publishable_xxx
VITE_FORMSPREE_URL=https://formspree.io/f/xxx
```

## Database Setup
Run `schema.sql` in Supabase SQL Editor.

## License
MIT — Built for builders 🚀