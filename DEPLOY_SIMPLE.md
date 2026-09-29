# Simple Deploy Steps (Hindi)

## 1. GitHub pe upload karein
- Ye folder (`hackathon rivals`) ko GitHub par naya repository bana ke push karein
- Ya GitHub Desktop use karein: "Add existing repository" → folder select → push

## 2. Netlify par deploy (sabse aasaan)
1. Netlify.com par account banaein
2. "Add new site" → "Import from Git" → GitHub select karein
3. Apna repository choose karein
4. Build settings automatically detect honge (static site)
5. **Environment variables** add karein (Site settings → Environment variables):
   ```
   VITE_SUPABASE_URL = https://xxx.supabase.co
   VITE_SUPABASE_ANON_KEY = sb_publishable_xxx
   VITE_FORMSPREE_URL = https://formspree.io/f/xxx (optional)
   ```
6. Deploy button dabao — 2 minute mein live ho jayega

## 3. Supabase setup
1. Supabase.com par project banaein
2. SQL Editor mein jaake `schema.sql` paste karke run karein
3. Storage → New bucket → name: `team-ppts` → Private → Create
4. Settings → API → URL aur Anon key copy karein (step 2 ke liye)

## 4. Icons banaein
- `generate-icons.html` browser mein kholein
- Dono buttons daba ke `icon-192.png` aur `icon-512.png` download karein
- Ye dono files folder mein daal dein

## 5. First Admin banaein
Supabase SQL Editor mein ye run karein (apna email daalein):
```sql
insert into profiles (id, email, full_name, role)
select id, email, 'Admin', 'Admin' from auth.users where email = 'aapka-email@college.edu';
```

## Bas! Live hai 🎉

### Test karein:
- `/` → Home page
- `/#register` → Team registration
- `/#arena` → Code Arena (login ke baad)
- `/#admin` → Admin dashboard (admin login ke baad)

### Problems?
- Netlify logs check karein (Functions → View logs)
- Browser console (F12) mein errors dekhein
- Supabase logs (Dashboard → Logs) check karein