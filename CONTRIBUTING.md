# Contributing to GTM Engineer Journey

First off, thank you for your interest in this project! This is primarily a personal learning journey, but I welcome contributions that align with the project's mission.

## 🎯 Project Mission

Building production-ready GTM tools while documenting the learning journey in public. The goal is to bridge the gap between GTM expertise and engineering capability.

## 🤝 How You Can Contribute

### 1. Share Ideas

Have ideas for GTM tools that would solve real pain points? Open an issue with:
- The problem you're trying to solve
- Who experiences this problem
- How you currently solve it (if at all)
- What an ideal solution would look like

### 2. Discuss AI/ML for Sales

Interested in AI applications for GTM? Let's discuss:
- Agent architectures for sales workflows
- LLM fine-tuning for domain-specific tasks
- Voice AI for discovery calls
- Data enrichment pipelines

### 3. Report Issues

Found a bug or security issue?
- **Security issues**: Email tkipper@gmail.com directly (do NOT open public issues)
- **Bugs**: Open an issue with steps to reproduce
- **Documentation**: Suggest improvements or clarifications

### 4. Code Contributions

**Note:** This is a learning repository, so code quality may vary as I'm actively learning. That said, if you want to contribute:

#### Before You Start
1. Open an issue to discuss your proposed changes
2. Wait for feedback before investing time in a PR
3. Make sure your contribution aligns with the learning journey theme

#### Development Setup
```bash
# Clone the repo
git clone https://github.com/ScientiaCapital/gtm-engineer-journey.git
cd gtm-engineer-journey

# Set up environment
cp .env.example .env
# Edit .env with your API keys (never commit this file!)

# For Python projects
cd projects/dealer-scraper-mvp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Code Standards

**Security (CRITICAL):**
- ✅ NEVER commit API keys, tokens, or credentials
- ✅ Always use `.env` for secrets
- ✅ Update `.gitignore` if adding new secret files
- ✅ Use `.env.example` with dummy values for documentation

**Code Quality:**
- Follow existing patterns in the codebase
- Add comments explaining "why" not just "what"
- Include error handling
- Test your changes

**Documentation:**
- Update README if changing functionality
- Add comments for complex logic
- Include usage examples

#### Pull Request Process

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/your-feature-name`
3. **Make your changes** (follow code standards above)
4. **Test thoroughly**
5. **Commit with clear messages:**
   ```bash
   git commit -m "Add: Feature description

   - What changed
   - Why it changed
   - Any breaking changes"
   ```
6. **Push to your fork:** `git push origin feature/your-feature-name`
7. **Open a Pull Request** with:
   - Clear description of changes
   - Why the changes are needed
   - How to test the changes
   - Screenshots (if UI changes)

## 🚫 What We Don't Accept

- **Low-effort PRs** (typo fixes without context, reformatting for no reason)
- **Scope creep** (adding features that don't align with GTM tools)
- **Breaking changes** without discussion first
- **Code that violates security best practices**

## 📚 Learning Resources

If you're also on a learning journey, here are resources I've found helpful:

**Python & APIs:**
- FastAPI docs (fastapi.tiangolo.com)
- Real Python (realpython.com)

**Docker:**
- Docker's official tutorial
- Docker Compose documentation

**AI/ML:**
- Anthropic Claude docs
- LangChain documentation
- HuggingFace tutorials

**GTM Context:**
- Books: Crossing the Chasm, Challenger Sale, Jobs to be Done
- My LEARNING_PLAN.md in this repo

## 💬 Communication

- **GitHub Issues:** Technical discussions, bug reports, feature requests
- **Email (tkipper@gmail.com):** Security issues, private discussions
- **LinkedIn:** General networking, career discussions

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You

Every contribution, no matter how small, helps make this learning journey better. Whether you're sharing an idea, reporting a bug, or just encouraging the journey - thank you!

---

**Remember:** This is a learning repository. Perfection is not the goal. Progress is.

<p align="center">
  <em>Building in Public • Learning in Public</em>
</p>
