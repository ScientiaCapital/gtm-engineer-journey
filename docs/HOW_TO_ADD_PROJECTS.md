# How to Add New Projects to Your Landing Page

Your landing page automatically loads projects from `docs/projects.json`. To add a new project, just edit that one file!

## Quick Start: Adding a New Project

1. Open `docs/projects.json`
2. Copy an existing project block
3. Update the fields for your new project
4. Save the file
5. Commit and push to GitHub
6. Your landing page auto-updates! 🎉

## Project Template

```json
{
  "id": "your-project-id",
  "name": "Your Project Name",
  "emoji": "🚀",
  "status": "live",
  "statusLabel": "✅ LIVE IN PRODUCTION",
  "description": "One-line quote about why you built this",
  "whatILearned": "Technologies and skills you learned",
  "metrics": [
    {
      "value": "1,000+",
      "label": "users"
    },
    {
      "value": "99%",
      "label": "uptime"
    }
  ],
  "techStack": ["Python", "FastAPI", "Docker", "React"],
  "demoLink": "demo.html",
  "githubLink": "https://github.com/YourUsername/your-repo"
}
```

## Field Guide

### Required Fields

- **id**: Unique identifier (use kebab-case: `my-cool-project`)
- **name**: Display name of your project
- **emoji**: Fun emoji to represent the project (🚀 🤖 📊 🔧 etc.)
- **status**: Project status - options:
  - `"live"` - Production, live users
  - `"in-progress"` - Currently building
  - `"exploring"` - Experimental/learning phase
- **statusLabel**: Badge text (e.g., "✅ LIVE", "🔄 IN PROGRESS", "🧪 EXPLORING")
- **description**: One-line quote explaining why you built it
- **whatILearned**: Technologies/skills you learned building this
- **techStack**: Array of technologies used (shows as badges)

### Optional Fields

- **metrics**: Array of metric objects to display
  - Each metric has `value` and `label`
  - Example: `{"value": "1,247", "label": "dealers scraped"}`
- **progress**: Number 0-100 for progress bar (only for in-progress projects)
- **demoLink**: Relative link to demo page (e.g., "my-demo.html")
- **githubLink**: Full GitHub URL to the project repo

## Example: Adding a Voice AI Project

Let's say you just shipped a Voice AI Sales Assistant. Here's how to add it:

```json
{
  "id": "voice-ai-assistant",
  "name": "Voice AI Sales Assistant",
  "emoji": "🎙️",
  "status": "live",
  "statusLabel": "✅ LIVE & PROCESSING CALLS",
  "description": "50+ daily calls were teaching me what AI should automate. So I built it.",
  "whatILearned": "Vapi, WebSockets, Real-time AI, Voice synthesis",
  "metrics": [
    {
      "value": "200+",
      "label": "calls processed"
    },
    {
      "value": "< 300ms",
      "label": "response time"
    }
  ],
  "techStack": ["Vapi", "WebSockets", "FastAPI", "React", "Anthropic Claude"],
  "demoLink": "voice-ai-demo.html",
  "githubLink": "https://github.com/ScientiaCapital/voice-ai-assistant"
}
```

Just add this to the `"projects"` array in `projects.json`, and your landing page will automatically show the new project!

## Status Badge Styling

The `status` field determines the badge color:
- `"live"` → Green badge (✅)
- `"in-progress"` → Orange/gold badge (🔄)
- `"exploring"` → Orange/gold badge (🧪)

## Tips for Great Project Entries

### 1. **Metrics Tell the Story**
Don't just say "scraping tool" - show the impact:
- ❌ "A web scraper"
- ✅ "1,247 dealers scraped, 99.2% success rate"

### 2. **Description = Your "Why"**
Make it personal and authentic:
- ❌ "A tool for data analysis"
- ✅ "When I was analyzing 50+ leads daily, I needed this. So I built it."

### 3. **Tech Stack = Learning Signal**
Show both depth and breadth:
- Include the full stack: Backend, Frontend, Infrastructure, AI
- Mix mature tech (Python, Docker) with bleeding edge (MCP, Claude)

### 4. **Progress Bars for Active Work**
If you're currently building something, add a progress bar:
```json
{
  "status": "in-progress",
  "progress": 65,
  "metrics": [
    {"value": "Week 3", "label": ""},
    {"value": "65%", "label": "Complete"}
  ]
}
```

## Workflow: From Code to Landing Page

1. **Build your project** (in `projects/your-project/`)
2. **Create a demo** (optional: `docs/your-project-demo.html`)
3. **Update projects.json** (add your new project)
4. **Commit everything**:
   ```bash
   git add docs/projects.json docs/your-demo.html
   git commit -m "Add Voice AI Assistant project"
   git push origin main
   ```
5. **Landing page auto-updates** (within 1-2 minutes)

## Complete Example: Your Current projects.json

See `docs/projects.json` for the current structure with all three projects:
- Dealer Scraper MVP (live)
- GTM Learning Journey (in-progress)
- AI Infrastructure (exploring)

Use these as templates when adding new projects!

---

**Questions?** The landing page code is in `docs/index.html` - search for the `loadProjects()` function to see how it renders the JSON.

**Pro Tip:** Keep your `projects.json` file organized chronologically (newest first) so your most recent work appears first on the landing page!
