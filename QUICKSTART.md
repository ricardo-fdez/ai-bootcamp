# 🚀 Quick Start Guide

Get "Emojis == Movie" running in 2 minutes!

## One-Line Start (Recommended)

### macOS/Linux
```bash
./start.sh
```

### Windows
```batch
start.bat
```

The scripts will automatically:
1. Create a virtual environment
2. Install dependencies
3. Create `.env` file
4. Start the server at http://localhost:8000

---

## Manual Start (3 Steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Server
```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Open Browser
```
http://localhost:8000
```

---

## First-Time Setup (Detailed)

### Step 1: Verify Python
```bash
python3 --version
# Should show 3.8 or higher
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows
```

### Step 3: Install Requirements
```bash
pip install -r requirements.txt
```

### Step 4: Run the App
```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

### Step 5: Play!
Open your browser to `http://localhost:8000` and start guessing movies! 🎬

---

## Quick Test

Verify the API is working:

```bash
# Health check
curl http://localhost:8000/health

# Get a puzzle
curl http://localhost:8000/api/puzzles?count=1

# Expected output: JSON with puzzle data
```

---

## Common Issues

**Port 8000 already in use?**
```bash
# Find what's using port 8000
lsof -i :8000        # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Use a different port
uvicorn src.app:app --host 0.0.0.0 --port 8001 --reload
# Then visit http://localhost:8001
```

**ModuleNotFoundError?**
```bash
# Make sure you're in the project directory
cd emoji-movie-app

# Reinstall dependencies
pip install -r requirements.txt
```

**Virtual environment not activating?**
```bash
# Delete and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## What's Next?

- 📖 Read [README.md](README.md) for full documentation
- 🎮 Play the game and enjoy guessing movies!
- 🎬 Add your own movies to `src/movies.json`
- 🚀 Deploy to Databricks Apps (see README)

---

**Have fun guessing! 🎉**

