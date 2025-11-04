# 🚀 Databricks Apps Deployment Guide

Complete checklist and instructions for deploying "Emojis == Movie" to Databricks Apps.

---

## 📋 Pre-Deployment Checklist

### ✅ Local Testing
- [ ] Application runs locally without errors
- [ ] Frontend loads at `http://localhost:8000`
- [ ] All API endpoints respond correctly
- [ ] Movies load and display properly
- [ ] Guess checking works correctly
- [ ] Health checks return 200 OK
- [ ] Run test suite: `./test_api.sh`

### ✅ File Verification
- [ ] `app.yaml` exists and is properly configured
- [ ] `requirements.txt` includes all dependencies
- [ ] `src/app.py` backend is working
- [ ] `src/movies.json` is valid JSON
- [ ] `public/index.html` frontend exists
- [ ] All files are under 10MB each
- [ ] No `.env` file in source (use .gitignore)

### ✅ Configuration Check
- [ ] Port is set to **8000** in `app.yaml`
- [ ] Command format uses array style: `["uvicorn", "src.app:app", ...]`
- [ ] Environment variables are properly set
- [ ] No hardcoded secrets in code
- [ ] CORS is enabled for frontend access

---

## 🔧 Databricks Setup

### Prerequisites
1. **Databricks Workspace** with Apps enabled
2. **Databricks CLI** installed and configured
3. **Permissions** to deploy apps in your workspace

### Install Databricks CLI
```bash
# Using pip
pip install databricks-cli

# Verify installation
databricks --version
```

### Configure CLI
```bash
# Configure authentication
databricks configure --token

# You'll be prompted for:
# - Databricks Host: https://your-workspace.cloud.databricks.com
# - Token: Your personal access token
```

### Verify Configuration
```bash
# Test connection
databricks workspace ls /

# Should list your workspace folders
```

---

## 📦 Deployment Steps

### Step 1: Test Locally (Final Check)
```bash
cd emoji-movie-app
./start.sh

# In another terminal:
./test_api.sh

# Verify all tests pass
```

### Step 2: Verify File Structure
```bash
# Your structure should look like:
emoji-movie-app/
├── app.yaml
├── requirements.txt
├── src/
│   ├── app.py
│   └── movies.json
└── public/
    └── index.html
```

### Step 3: Deploy to Databricks Apps
```bash
databricks apps deploy emoji-movie-app \
    --source-code-path /path/to/emoji-movie-app
```

**Note**: Replace `/path/to/emoji-movie-app` with actual absolute path

Example:
```bash
databricks apps deploy emoji-movie-app \
    --source-code-path /Users/yourname/projects/emoji-movie-app
```

### Step 4: Monitor Deployment
```bash
# Check deployment status
databricks apps list

# View app details
databricks apps get emoji-movie-app

# Check logs
databricks apps logs emoji-movie-app
```

### Step 5: Verify Deployment
Once deployed, you'll receive an app URL like:
```
https://your-workspace.cloud.databricks.com/apps/emoji-movie-app
```

Test the deployment:
```bash
# Replace with your actual app URL
APP_URL="https://your-workspace.cloud.databricks.com/apps/emoji-movie-app"

# Health check
curl $APP_URL/health

# Get puzzles
curl $APP_URL/api/puzzles?count=1

# Open in browser
open $APP_URL  # macOS
# OR
start $APP_URL  # Windows
```

---

## 🔍 Troubleshooting Deployment

### Issue: Deployment Fails

**Check app.yaml syntax:**
```yaml
# Correct format (array style)
command: [
  "uvicorn",
  "src.app:app",
  "--host", "0.0.0.0",
  "--port", "8000"
]

# Wrong format (string style) - DON'T USE
command: "uvicorn src.app:app --host 0.0.0.0 --port 8000"
```

**Verify file sizes:**
```bash
# Check individual file sizes
find . -type f -exec ls -lh {} \; | awk '{print $5, $9}' | grep -v "\.git"

# Each file must be < 10MB
```

### Issue: App Starts but Returns 500 Error

**Check logs:**
```bash
databricks apps logs emoji-movie-app --lines 100
```

**Common causes:**
- File paths incorrect (check path resolution in app.py)
- Missing dependencies in requirements.txt
- Invalid JSON in movies.json
- Port mismatch (must be 8000)

**Debug endpoint:**
```bash
curl https://your-app-url/debug
```

### Issue: Frontend Not Loading

**Verify file paths:**
```python
# In src/app.py, check path resolution:
possible_paths = [
    Path(__file__).parent.parent / "public" / "index.html",
    Path("public/index.html"),
    Path("/app/public/index.html"),  # Container path
]
```

**Check static files serving:**
```bash
# Test if frontend is accessible
curl https://your-app-url/ -I

# Should return 200 OK with text/html content-type
```

### Issue: CORS Errors

**Verify CORS configuration in app.py:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: Movies Not Loading

**Check movies.json:**
```bash
# Validate JSON syntax
python3 -m json.tool src/movies.json > /dev/null

# Should not show any errors
```

**Verify file exists in deployment:**
```bash
# Check debug endpoint
curl https://your-app-url/debug

# Look for "movies_json_exists": true
```

---

## 🔄 Updating Your Deployment

### Make Changes Locally
1. Edit files locally
2. Test changes: `./start.sh` and `./test_api.sh`
3. Verify everything works

### Redeploy
```bash
# Deploy updated version
databricks apps deploy emoji-movie-app \
    --source-code-path /path/to/emoji-movie-app

# Monitor update
databricks apps logs emoji-movie-app --follow
```

### Rollback (if needed)
```bash
# Delete current deployment
databricks apps delete emoji-movie-app

# Redeploy previous version
databricks apps deploy emoji-movie-app \
    --source-code-path /path/to/previous-version
```

---

## 📊 Monitoring Your App

### Health Checks
Set up monitoring on these endpoints:
- `/health` - Basic health check
- `/healthz` - Kubernetes-style health
- `/ready` - Readiness probe
- `/metrics` - Prometheus metrics

### Example Monitoring Script
```bash
#!/bin/bash
APP_URL="https://your-app-url"

while true; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" $APP_URL/health)
    if [ "$STATUS" = "200" ]; then
        echo "$(date): ✅ App is healthy"
    else
        echo "$(date): ❌ App is down (HTTP $STATUS)"
    fi
    sleep 60
done
```

### View Logs
```bash
# Live logs
databricks apps logs emoji-movie-app --follow

# Last 100 lines
databricks apps logs emoji-movie-app --lines 100

# Search for errors
databricks apps logs emoji-movie-app | grep ERROR
```

---

## 🔐 Security Best Practices

### Don't Include in Source Code
- ❌ `.env` files
- ❌ API tokens
- ❌ Passwords
- ❌ Private keys

### Use Databricks Secrets
If you need secrets (for future features):
```yaml
# In app.yaml
env:
  - name: 'API_KEY'
    valueFrom: my_secret_key
```

Then create the secret in Databricks:
```bash
databricks secrets create-scope --scope my-scope
databricks secrets put --scope my-scope --key my_secret_key
```

---

## 📈 Performance Optimization

### For Production
1. **Enable Caching**: Movies are already cached in memory
2. **Rate Limiting**: Add rate limiting middleware if needed
3. **CDN**: Frontend assets served via CDN already
4. **Monitoring**: Set up health check alerts
5. **Logging**: Review logs regularly for errors

### Scaling
Databricks Apps automatically handles scaling based on load.

---

## 🧪 Post-Deployment Testing

```bash
# Set your app URL
export APP_URL="https://your-app-url"

# Test suite
echo "Testing $APP_URL"

# Health
curl $APP_URL/health

# API endpoints
curl $APP_URL/api/puzzles?count=1
curl $APP_URL/api/daily
curl $APP_URL/metrics

# Frontend
curl -I $APP_URL/

# Guess checking
curl -X POST $APP_URL/api/guess \
  -H "Content-Type: application/json" \
  -d '{"puzzle_id":"lnk-1994-ez","guess":"the lion king"}'

echo "✅ All tests complete!"
```

---

## 📞 Support & Help

### Databricks Apps Documentation
- [Databricks Apps Guide](https://docs.databricks.com/apps/)
- [Deployment Best Practices](https://docs.databricks.com/apps/deployment.html)

### Common Issues
1. **Port must be 8000** - Don't change this!
2. **Files must be <10MB** - Check sizes before deploying
3. **Command must be array** - Use `["cmd", "arg1", "arg2"]` format
4. **Paths matter** - Use multiple path resolution strategies

### Getting Help
1. Check logs: `databricks apps logs emoji-movie-app`
2. Test `/debug` endpoint
3. Review this deployment guide
4. Check Databricks Apps documentation

---

## ✅ Deployment Success Checklist

After deployment, verify:
- [ ] App URL is accessible
- [ ] `/health` endpoint returns 200
- [ ] Frontend loads in browser
- [ ] Puzzles display correctly
- [ ] Guessing works
- [ ] Hints reveal properly
- [ ] Timer counts down
- [ ] Score updates
- [ ] Daily mode works
- [ ] No console errors
- [ ] Mobile responsive
- [ ] Keyboard shortcuts work

---

## 🎉 You're Live!

Congratulations! Your "Emojis == Movie" game is now deployed on Databricks Apps!

Share your app URL with friends and colleagues to play!

**Next Steps:**
- Add more movies to `src/movies.json`
- Customize the UI colors/theme
- Add new features from ROADMAP
- Monitor usage and performance
- Gather user feedback

---

**Happy Deploying! 🚀🎬**

