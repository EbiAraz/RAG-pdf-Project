# GitHub & HuggingFace Setup Guide

## 📊 Current Status

✅ **Git Repository Initialized**
✅ **23 Files Committed**
✅ **.gitignore Configured**
✅ **Ready for GitHub Push**

---

## 🚀 Step 1: Push to GitHub

### If you have an existing GitHub repository:

```bash
# Navigate to project
cd c:\Users\Ebi_Mahmdli\Desktop\rag_pdf_project

# Add GitHub remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/rag_pdf_project.git

# Rename branch to main (optional but recommended)
git branch -M main

# Push to GitHub
git push -u origin main
```

### If you need to create a new GitHub repository:

1. Go to https://github.com/new
2. Create a new repository named `rag_pdf_project`
3. Copy the repository URL
4. Run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/rag_pdf_project.git
git branch -M main
git push -u origin main
```

---

## 🤖 Step 2: Deploy to HuggingFace Spaces

### Option A: Easy Setup (Recommended)

1. Go to https://huggingface.co/spaces/create
2. Select **Space SDK: Gradio**
3. Name it `rag-pdf-assistant`
4. Click **Create Space**
5. Upload the repository files or clone this repo

### Option B: Command Line Setup

```bash
# 1. Install huggingface-hub if not already installed
pip install huggingface-hub

# 2. Login to HuggingFace (get token from https://huggingface.co/settings/tokens)
huggingface-cli login

# 3. Create a new Space repository
huggingface-cli repo create rag-pdf-assistant --type space --space-sdk docker

# 4. Add HuggingFace as remote
git remote add hf https://huggingface.co/spaces/YOUR_HF_USERNAME/rag-pdf-assistant

# 5. Push to HuggingFace Spaces
git push hf main
```

### Option C: GitHub Actions (Auto-Deploy)

Create `.github/workflows/deploy-to-huggingface.yml`:

```yaml
name: Deploy to HuggingFace Spaces

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Push to HuggingFace
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          git config --global user.email "action@github.com"
          git config --global user.name "GitHub Action"
          git remote add hf https://huggingface-ci:$HF_TOKEN@huggingface.co/spaces/YOUR_HF_USERNAME/rag-pdf-assistant
          git push hf main --force
```

Then add your HF_TOKEN to GitHub Secrets.

---

## 📝 GitHub Repository Files

Your repository now includes:

```
✅ README.md              - Project overview with HF info
✅ LICENSE               - MIT License
✅ .gitignore            - Excludes cache, models, .venv
✅ .env.example          - Environment variables template
✅ requirements.txt      - All dependencies
✅ QUICK_START.md        - Quick start guide
✅ TECHNICAL_DOCS.md     - Architecture documentation
✅ EXAMPLES_AND_TESTS.md - Examples and debugging
✅ PROJECT_STATUS.md     - Project completion report
✅ app.py                - Main Gradio application
✅ main.py               - CLI alternative
✅ All source code files
```

---

## 🎯 HuggingFace Spaces Configuration

The project is already configured for HuggingFace Spaces with:

### ✅ Already Configured in README.md

```yaml
---
title: RAG PDF Assistant
emoji: 📄
colorFrom: blue
colorTo: indigo
sdk: gradio
app_file: app.py
pinned: true
---
```

### ✅ Gradio App Ready

- `app.py` is the main entry point
- Gradio interface configured
- Models auto-download on first run
- HuggingFace models used (transformers, sentence-transformers)

### ✅ Docker Compatible

The project works with HuggingFace's Docker deployment:
- Python 3.10+ compatible
- All dependencies in requirements.txt
- No external API keys required (models on HuggingFace Hub)

---

## 🔐 Environment Variables

For local development, create `.env`:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```
HF_TOKEN=your_huggingface_token
GRADIO_SHARE=False
GRADIO_SERVER_PORT=7860
```

---

## 📊 Git Commands Reference

### Check git status
```bash
cd c:\Users\Ebi_Mahmdli\Desktop\rag_pdf_project
git status
```

### View commit history
```bash
git log --oneline
```

### Make changes and commit
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

### Push to multiple remotes
```bash
git push origin main        # GitHub
git push hf main            # HuggingFace Spaces
```

---

## 🚀 Deployment Checklist

- [ ] GitHub repository created
- [ ] Git remote added (`git remote -v` shows origin)
- [ ] Code pushed to GitHub (`git push origin main`)
- [ ] HuggingFace Spaces repository created
- [ ] HuggingFace remote added
- [ ] Code pushed to HuggingFace (`git push hf main`)
- [ ] Space deployed successfully
- [ ] App accessible at `https://huggingface.co/spaces/YOUR_USERNAME/rag-pdf-assistant`

---

## 📱 Share Your Project

### Share GitHub Repository
```
https://github.com/YOUR_USERNAME/rag_pdf_project
```

### Share HuggingFace Spaces
```
https://huggingface.co/spaces/YOUR_HF_USERNAME/rag-pdf-assistant
```

### Create a Shortlink
- GitHub: Use GitHub's built-in shortened URLs
- HuggingFace: Use bit.ly or short.link services

---

## 🤝 Collaboration

### Invite Collaborators (GitHub)
1. Go to repository Settings
2. Click "Manage access"
3. Click "Invite teams or people"
4. Add collaborator email

### Share HuggingFace Space
1. HuggingFace Spaces are public by default
2. Anyone can use the web UI
3. Community members can fork and create derivatives

---

## 📈 Monitor Your Deployment

### GitHub
- Check "Insights" tab for statistics
- View "Actions" for workflow status
- Monitor "Issues" and "Discussions"

### HuggingFace Spaces
- Check app logs in Space settings
- View traffic statistics
- See community comments

---

## 🔄 Continuous Updates

### Update from GitHub
```bash
# Make changes locally
git add .
git commit -m "Fix: issue description"
git push origin main

# Also push to HuggingFace
git push hf main
```

### Pull from GitHub (if working on multiple machines)
```bash
git pull origin main
```

---

## 🆘 Troubleshooting

### Issue: "fatal: not a git repository"
- **Solution**: Make sure you're in project directory
  ```bash
  cd c:\Users\Ebi_Mahmdli\Desktop\rag_pdf_project
  ```

### Issue: "Permission denied" when pushing
- **Solution**: Check GitHub credentials
  ```bash
  git config --list | grep url
  ```

### Issue: "Branch 'main' not found"
- **Solution**: Rename branch
  ```bash
  git branch -M main
  ```

### Issue: HuggingFace Space deployment fails
- **Solution**: Check app.py and requirements.txt are in root
- Ensure no API keys hardcoded in code
- Check models are from HuggingFace Hub

---

## 📞 Next Steps

1. **Create GitHub repository** (if not already created)
2. **Push code to GitHub**
3. **Create HuggingFace Space**
4. **Deploy to HuggingFace Spaces**
5. **Share the links with your team!**

---

## 🎉 Project Status

**Repository**: ✅ Initialized and committed
**GitHub**: ⏳ Awaiting push
**HuggingFace**: ⏳ Awaiting setup
**Documentation**: ✅ Complete
**Application**: ✅ Running and tested

Ready to push! 🚀
