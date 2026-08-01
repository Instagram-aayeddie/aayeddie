# aayeddie-studio

Personal portfolio site for @aayeddie, plus a self-contained admin panel for editing it — no backend, no build step, no vendor lock-in.

## 🚀 Live Site

Once GitHub Pages is enabled (see below), your site is live at:

```
https://<your-username>.github.io/<your-repo>/
```

## 📁 What's in here

| File | Purpose |
|---|---|
| `index.html` | The public portfolio site (hero, highlights, social hub, project gallery). |
| `admin.html` | A local/private control panel: live preview + edit pencils, PFP & theme editor, highlight/slide manager, social channel manager, JSON export, and a repo-setup helper. **Do not link to this from the public site** — it's a tool for you, not visitors. |
| `data.json` | The site's committed default content (hero text, theme colors, socials, highlights). `index.html` fetches this on load. |
| `.github/workflows/deploy.yml` | GitHub Actions workflow that deploys the repo to GitHub Pages on every push to `main`. |

## 🧠 How content updates actually work

`index.html` loads content in two layers:

1. **`data.json`** (committed to the repo) — this is what every visitor sees.
2. **`localStorage`** in your own browser — instant local overrides used by `admin.html` for live-previewing changes before you commit them.

So the flow to make a permanent change live for everyone is:

1. Open `admin.html` (works locally by double-clicking it, or from the deployed site).
2. Edit hero text, PFP, colors, socials, or highlight rings — the live preview updates instantly (in your browser only, via `localStorage`).
3. Go to the **JSON Data Sync & Backup** tab → **Download data.json**.
4. Replace the `data.json` file in the repo root with the downloaded one.
5. Commit and push. GitHub Actions redeploys automatically, and the new content is now the default for all visitors.

If you skip steps 3–5, your edits only ever exist in your own browser's `localStorage` — fine for previewing, but they won't appear for anyone else or survive clearing site data.

## 🛠️ Local preview

Because `index.html` fetches `data.json` via `fetch()`, opening the file directly as `file://` will have that request blocked by the browser in some cases. To preview locally with everything working, serve the folder instead:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000/
```

## 📦 First-time GitHub setup

```bash
git init
git add .
git commit -m "Initial commit: portfolio site + admin panel"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

Then in the repo on GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**. The included workflow handles the rest.

## 🎨 Customizing without the admin panel

You can also hand-edit `data.json` directly — it's a plain JSON file with `pfp`, `hero`, `theme`, `socials`, and `highlights` keys, matching what the admin panel exports.
