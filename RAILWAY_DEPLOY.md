# Railway Deployment Guide - Quick Start

## 🚀 Quick Deploy Steps

### Option 1: Railway Dashboard (Recommended)

1. **Go to Railway**
   - Visit [railway.app](https://railway.app)
   - Sign in or create account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo" (if you have a repo)
   - OR select "Empty Project" to deploy from local

3. **Configure Service**
   - If deploying from GitHub:
     - Select your repository
     - Set **Root Directory** to: `streamlit-ui`
   - If deploying from local:
     - Use Railway CLI (see Option 2)

4. **Set Environment Variables**
   In Railway dashboard → Your Service → Variables:
   ```
   N8N_WEBHOOK_BASE_URL=https://primary-production-10917.up.railway.app/webhook
   ```
   
   Railway will automatically set `PORT` variable - no need to set it manually.

5. **Deploy**
   - Railway will auto-detect the Dockerfile
   - Build will start automatically
   - Monitor the build logs

6. **Access Your App**
   - Railway provides a URL (e.g., `https://your-app.up.railway.app`)
   - Click "Generate Domain" for a custom URL

---

### Option 2: Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Navigate to project
cd streamlit-ui

# Initialize Railway project
railway init

# Set environment variable
railway variables set N8N_WEBHOOK_BASE_URL=https://primary-production-10917.up.railway.app/webhook

# Deploy
railway up
```

---

## ✅ Verification Checklist

After deployment:

- [ ] Application URL is accessible
- [ ] Home page loads
- [ ] Dashboard page loads
- [ ] API connection works (check Settings page)
- [ ] All pages navigate correctly
- [ ] No errors in Railway logs

---

## 🔧 Troubleshooting

### Build Fails
- Check Railway build logs
- Verify Dockerfile syntax
- Ensure all files are in `streamlit-ui` directory

### App Won't Start
- Check Railway logs
- Verify `PORT` variable is set (Railway sets this automatically)
- Verify `N8N_WEBHOOK_BASE_URL` is correct

### API Errors
- Verify n8n workflows are active
- Check webhook URL is correct
- Test API endpoint directly

---

## 📝 Environment Variables

**Required:**
- `N8N_WEBHOOK_BASE_URL` - Your n8n webhook base URL

**Optional (have defaults):**
- `STREAMLIT_SERVER_PORT` - Default: 8501 (Railway sets PORT automatically)
- `STREAMLIT_SERVER_ADDRESS` - Default: 0.0.0.0
- `CACHE_TTL_MINUTES` - Default: 5
- `ITEMS_PER_PAGE` - Default: 50

**Note:** Railway automatically provides `PORT` environment variable - the app will use it.

---

## 🎉 Success!

Once deployed, your app will be live at the Railway-provided URL!

