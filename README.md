# AI-Caller Streamlit UI

A modern Streamlit web application for managing AI-powered calling campaigns, leads, and analytics.

## Features

- 📊 **Dashboard** - Real-time stats and performance metrics
- 👥 **Lead Management** - Create, update, and manage leads
- 📞 **Call History** - View and analyze call records
- 📈 **Campaigns** - Monitor campaign performance
- ⚙️ **Settings** - Configure preferences

## Setup

### Prerequisites

- Python 3.11+
- Access to n8n webhook endpoints

### Installation

1. Clone the repository
2. Navigate to the `streamlit-ui` directory
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```
6. Edit `.env` with your n8n webhook base URL

### Running Locally

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Deployment

### Railway

#### Quick Start

1. **Create New Railway Project**
   - Go to [Railway](https://railway.app)
   - Create a new project
   - Select "Deploy from GitHub repo" or "Empty Project"

2. **Connect Repository**
   - If using GitHub: Connect your repository
   - Select the `streamlit-ui` directory as the root
   - Or deploy from local directory using Railway CLI

3. **Configure Environment Variables**
   In Railway dashboard, add these environment variables:
   ```bash
   N8N_WEBHOOK_BASE_URL=https://primary-production-10917.up.railway.app/webhook
   STREAMLIT_SERVER_PORT=8501
   STREAMLIT_SERVER_ADDRESS=0.0.0.0
   ```

4. **Deploy**
   - Railway will automatically detect the Dockerfile
   - Build and deploy will start automatically
   - Monitor the deployment logs

5. **Access Your App**
   - Railway will provide a URL (e.g., `https://your-app.railway.app`)
   - The app will be available immediately after deployment

#### Using Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
cd streamlit-ui
railway init

# Set environment variables
railway variables set N8N_WEBHOOK_BASE_URL=https://your-url.com/webhook

# Deploy
railway up
```

#### Custom Domain (Optional)

1. In Railway dashboard, go to your service
2. Click "Settings" → "Generate Domain" or "Custom Domain"
3. Follow the DNS configuration instructions
4. SSL certificate will be automatically provisioned

For detailed deployment instructions, see [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md).

## Project Structure

```
streamlit-ui/
├── app.py                 # Main application entry point
├── pages/                 # Multi-page app pages
├── utils/                 # Utility modules
│   ├── config.py         # Configuration management
│   ├── api_client.py     # n8n API client
│   ├── helpers.py        # Helper functions
│   └── styling.py        # CSS and theming
├── components/           # Reusable components
│   ├── ui/               # UI components
│   └── layout/           # Layout components
├── assets/               # Static assets (CSS, images)
└── requirements.txt      # Python dependencies
```

## Configuration

See `.env.example` for available configuration options.

## License

Proprietary - All rights reserved

