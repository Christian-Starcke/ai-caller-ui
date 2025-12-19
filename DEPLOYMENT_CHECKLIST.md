# Railway Deployment Checklist

## Pre-Deployment

### 1. Environment Variables
- [ ] `N8N_WEBHOOK_BASE_URL` - Set to your n8n webhook base URL
- [ ] `STREAMLIT_SERVER_PORT` - Set to `8501` (or Railway's PORT variable)
- [ ] `STREAMLIT_SERVER_ADDRESS` - Set to `0.0.0.0`
- [ ] `CACHE_TTL_MINUTES` - Optional (default: 5)
- [ ] `ITEMS_PER_PAGE` - Optional (default: 50)
- [ ] `API_TIMEOUT_SECONDS` - Optional (default: 30)
- [ ] `API_RETRY_ATTEMPTS` - Optional (default: 3)

### 2. Code Review
- [ ] All dependencies listed in `requirements.txt`
- [ ] No hardcoded credentials or API keys
- [ ] Error handling implemented
- [ ] All imports working correctly
- [ ] No syntax errors

### 3. Local Testing
- [ ] Application runs locally without errors
- [ ] All pages load correctly
- [ ] API connections work
- [ ] Forms submit successfully
- [ ] Charts render properly

## Railway Setup

### 1. Create New Project
- [ ] Create new Railway project
- [ ] Name it appropriately (e.g., "ai-caller-ui")
- [ ] Select the correct team/organization

### 2. Connect Repository
- [ ] Connect GitHub/GitLab repository
- [ ] Select the `streamlit-ui` directory as root
- [ ] Or deploy from local directory

### 3. Configure Build
- [ ] Railway should auto-detect Dockerfile
- [ ] Verify `railway.json` is in root
- [ ] Check build settings

### 4. Set Environment Variables
- [ ] Add all required environment variables in Railway dashboard
- [ ] Use Railway's `$PORT` variable for port (if available)
- [ ] Verify `N8N_WEBHOOK_BASE_URL` is correct

### 5. Deploy
- [ ] Trigger initial deployment
- [ ] Monitor build logs
- [ ] Check for build errors
- [ ] Verify deployment succeeds

## Post-Deployment

### 1. Testing
- [ ] Access application URL
- [ ] Test all pages load
- [ ] Test API connections
- [ ] Test form submissions
- [ ] Test CSV upload
- [ ] Check error handling

### 2. Monitoring
- [ ] Check Railway logs for errors
- [ ] Monitor resource usage
- [ ] Set up alerts (optional)
- [ ] Check application health

### 3. Custom Domain (Optional)
- [ ] Add custom domain in Railway
- [ ] Configure DNS settings
- [ ] Verify SSL certificate
- [ ] Test domain access

## Troubleshooting

### Common Issues

**Build Fails:**
- Check Dockerfile syntax
- Verify all dependencies in requirements.txt
- Check Python version compatibility

**Application Won't Start:**
- Verify PORT environment variable
- Check server address is `0.0.0.0`
- Review startup logs

**API Errors:**
- Verify `N8N_WEBHOOK_BASE_URL` is correct
- Check n8n workflows are active
- Test API endpoints directly

**Styling Issues:**
- Verify CSS file is included
- Check asset paths are correct
- Clear browser cache

## Quick Deploy Commands

### Using Railway CLI
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Link to existing project
railway link

# Set environment variables
railway variables set N8N_WEBHOOK_BASE_URL=https://your-url.com/webhook

# Deploy
railway up
```

### Manual Deployment
1. Push code to Git repository
2. Connect repository in Railway dashboard
3. Set environment variables
4. Deploy

## Environment Variables Reference

```bash
# Required
N8N_WEBHOOK_BASE_URL=https://primary-production-10917.up.railway.app/webhook

# Optional (with defaults)
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
CACHE_TTL_MINUTES=5
ITEMS_PER_PAGE=50
API_TIMEOUT_SECONDS=30
API_RETRY_ATTEMPTS=3
```

## Support

If you encounter issues:
1. Check Railway deployment logs
2. Review application logs
3. Test API endpoints directly
4. Verify environment variables
5. Check n8n workflow status

---

**Last Updated:** 2025-12-19

