# GTM Engineer Journey

## What This Repository Is

**This is a learning journal and portfolio showcase** - documenting the journey from 25+ years GTM executive to high-caliber GTM Engineer. This repo is NOT where projects are built - it's where the journey is documented and showcased publicly via GitHub Pages.

**Live Portfolio:** [scientiacapital.github.io/gtm-engineer-journey](https://scientiacapital.github.io/gtm-engineer-journey)

## The 5 Production Projects (Built Elsewhere)

All actual project code lives in separate repositories at `/tk_projects/`:

### 1. Sales Agent (`/tk_projects/sales-agent`)
**Repo:** [ScientiaCapital/sales-agent](https://github.com/ScientiaCapital/sales-agent)
**What:** Enterprise AI sales automation with 6 specialized LangGraph agents
**Stack:** FastAPI, LangGraph, PostgreSQL, Redis, Cerebras, Claude, Close CRM
**Status:** Phase 6 - Pipeline Testing
**Metrics:** ~12s pipeline, $0.000006/lead, 96% test coverage

### 2. Dealer Scraper MVP (`/tk_projects/dealer-scraper-mvp`)
**Repo:** [ScientiaCapital/dealer-scraper-mvp](https://github.com/ScientiaCapital/dealer-scraper-mvp)
**What:** Multi-OEM contractor intelligence with ICP scoring
**Stack:** Python, BeautifulSoup, Pandas, Streamlit, Playwright
**Status:** Live & Processing
**Metrics:** 8,277 contractors, 97.3% dedup, 198 multi-OEM prospects

### 3. Swaggy Stacks (`/tk_projects/swaggy-stacks`)
**Repo:** [ScientiaCapital/swaggy-stacks](https://github.com/ScientiaCapital/swaggy-stacks)
**What:** Institutional-grade algorithmic trading platform
**Stack:** FastAPI, Next.js 14, PostgreSQL, Grafana, Prometheus, Alpaca API
**Status:** Production-Ready
**Metrics:** 359 Python modules, 11 options strategies, 6 Grafana dashboards

### 4. AI Cost Optimizer (`/tk_projects/ai-cost-optimizer`)
**Repo:** [ScientiaCapital/ai-cost-optimizer](https://github.com/ScientiaCapital/ai-cost-optimizer)
**What:** Intelligent LLM routing for 40-70% cost savings
**Stack:** FastAPI, MCP, SQLite, multi-provider (Anthropic, Google, Cerebras, DeepSeek)
**Status:** MCP Marketplace Ready
**Metrics:** 40+ models, 8 providers, real-time cost tracking

### 5. ThetaRoom (`/tk_projects/thetaroom`)
**Repo:** [ScientiaCapital/ThetaRoom](https://github.com/ScientiaCapital/ThetaRoom)
**What:** GPU-accelerated autonomous AI trading platform
**Stack:** FastAPI, Next.js 15, FlashAttention-3, GraphRAG, Neon, Alpaca API
**Status:** Deployment Ready
**Metrics:** 352 Python files, <$250/month, 24/7 autonomous ops

## This Repository Structure

```
gtm-engineer-journey/
├── docs/                      # GitHub Pages (PUBLIC portfolio)
│   ├── index.html            # Main landing page
│   ├── projects.json         # ALL 5 projects data
│   └── projects/             # Individual demo pages
├── learning-logs/            # Personal learning reflections (optional: private)
├── milestones/               # Major achievements
├── resources/                # Books, tools, courses
├── templates/                # Consistency helpers
├── scripts/                  # Automation tools
└── archive/                  # Historical reference projects
```

## Critical Rules for This Repo

Since this is a **learning journal**, not active development:

### When Working Here
- ✅ Update portfolio when projects reach milestones
- ✅ Document learning in `learning-logs/`
- ✅ Capture breakthroughs in `milestones/`
- ✅ Keep `docs/projects.json` current with project progress
- ✅ Use templates for consistency

### When NOT Working Here
- ❌ Don't write project code here (it lives in separate repos)
- ❌ Don't duplicate documentation from project repos
- ❌ Don't let portfolio get stale (update monthly minimum)

## Global Project Rules (Apply to All 5 Projects)

When working on ANY of the 5 projects:

### Security
- ❌ **Never use OpenAI** - Use Claude/Anthropic APIs only
- ❌ **API keys ONLY in .env** - Never hardcode

### Code Quality
- ✅ Type hints on all Python functions
- ✅ GTM terminology in docstrings (sales workflows, not generic CS terms)
- ✅ Production-ready error handling
- ✅ Comprehensive testing

### Stack Consistency
- **Backend:** Python, FastAPI
- **Database:** PostgreSQL, Redis
- **AI/LLM:** Claude, Cerebras, DeepSeek (NO OpenAI)
- **Frontend:** Next.js, TypeScript, Tailwind CSS

## Portfolio Maintenance

Update `docs/projects.json` when:
- Project reaches new milestone
- Metrics change significantly
- Status changes (exploring → live, etc.)
- New projects added

Use `/templates/project-entry.json` as template for new projects.

## Purpose: Learning Journey → High-Caliber GTME

**Goal:** Document transition from GTM executive to GTM Engineer who can both build and sell AI-native tools.

**Target Audience:**
- Potential employers (technical GTM roles)
- GTM community (building in public)
- Future self (learning documentation)

**Not a Goal:**
- Commercial product development (that's in project repos)
- Tutorial content (that's not the point)
- Code portfolio (that's what GitHub profiles are for)

This is about **documenting the journey** - the struggles, breakthroughs, and growth from Day 1 to becoming a high-caliber GTME.
