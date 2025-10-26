# Setting Up Your GTM Engineer Portfolio

## 📁 Repository Structure

```
gtm-engineer-journey/
├── README.md                 # Main portfolio page
├── index.html               # GitHub Pages home
├── LEARNING_PLAN.md         # Your 6-month plan
├── .gitignore              # Ignore files
├── docs/                   # GitHub Pages content
│   ├── index.html         # Portfolio site
│   ├── style.css
│   └── demos/             # Live demos here
├── week01-docker-api/      # Week 1 project
│   ├── README.md
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── src/
├── week02-auth-system/     # Week 2 project
├── week03-fullstack/       # Week 3 project
├── week04-production/      # Week 4 project
├── updates/                # Weekly progress logs
│   ├── week01.md
│   └── week02.md
├── notes/                  # Learning notes
│   ├── docker.md
│   ├── fastapi.md
│   └── production.md
└── snippets/              # Reusable code
```

## 🚀 Quick Setup

### 1. Initialize Git Repository
```bash
cd /Users/tmkipper/Desktop/tk_projects/gtm-engineer-journey
git init
git add .
git commit -m "Initial commit: GTM Engineer Journey"
```

### 2. Create GitHub Repository
1. Go to GitHub.com
2. New repository: `gtm-engineer-journey`
3. Make it PUBLIC (for GitHub Pages)
4. Don't add README (we have one)

### 3. Push to GitHub
```bash
git remote add origin https://github.com/ScientiaCapital/gtm-engineer-journey.git
git branch -M main
git push -u origin main
```

### 4. Enable GitHub Pages
1. Go to Settings → Pages
2. Source: Deploy from branch
3. Branch: main, folder: `/docs`
4. Save

Your portfolio will be live at:
**https://ScientiaCapital.github.io/gtm-engineer-journey**

## 📝 Weekly Workflow

### Every Day:
1. Create daily work in appropriate week folder
2. Commit with descriptive message:
   ```bash
   git add .
   git commit -m "Day 1: Docker basics - created first Dockerfile"
   git push
   ```

### Every Week:
1. Update main README with progress
2. Add demo link when deployed
3. Create week summary in `/updates/`
4. Tag weekly release:
   ```bash
   git tag -a week1 -m "Week 1 complete: Docker stack"
   git push --tags
   ```

## 🎯 Deploy Strategy

### Free Hosting Options:
- **GitHub Pages**: Portfolio site (static)
- **Railway.app**: FastAPI backends (free tier)
- **Vercel**: React/Next.js apps (free)
- **Render**: Full-stack apps (free tier)
- **Supabase**: PostgreSQL database (free)
- **Upstash**: Redis (serverless free tier)

### Week 1 Deployment Example:
```bash
# Deploy to Railway
cd week01-docker-api
railway login
railway init
railway up
# Get URL: https://your-api.railway.app
```

## 📊 Interview Preparation

### What to Show:
1. **Live Demos**: All projects deployed
2. **Code Quality**: Clean, documented code
3. **Progress**: Consistent GitHub commits
4. **Learning**: Notes and blog posts
5. **Architecture**: Diagrams in READMEs

### Portfolio Checklist:
- [ ] Custom domain (optional): gtm-engineer.com
- [ ] Professional README
- [ ] Live demo links
- [ ] Architecture diagrams
- [ ] Performance metrics
- [ ] Blog posts/tutorials

## 🔗 Important Links

- **Portfolio**: https://ScientiaCapital.github.io/gtm-engineer-journey
- **GitHub**: https://github.com/ScientiaCapital/gtm-engineer-journey
- **Week 1 Demo**: [Coming Monday]
- **Blog**: [Add your blog URL]

## 💡 Tips

1. **Commit Daily**: Show consistent progress
2. **Document Everything**: READMEs are crucial
3. **Deploy Weekly**: Even simple apps
4. **Add Metrics**: Response times, uptime
5. **Use Issues**: Track your TODOs
6. **Create Releases**: For major milestones

---

Start Monday with confidence! 🚀
