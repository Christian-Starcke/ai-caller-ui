# AI-Caller Streamlit UI

A simple Streamlit web application for managing AI-powered calling campaigns.

## Features

- 📊 **Dashboard** - View stats and system status
- 👥 **Leads** - Manage leads and contacts
- 📞 **Calls** - View call history
- ⚙️ **Settings** - Configure API settings

## Setup

### Prerequisites

- Python 3.8+
- Access to n8n webhook endpoints

### Installation

1. Navigate to the `streamlit-ui` directory
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your n8n webhook URL:
   ```bash
   N8N_WEBHOOK_BASE_URL=https://your-n8n-url.com/webhook
   ```

### Running Locally

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Deployment

### Railway

1. **Create New Railway Project**
   - Go to [Railway](https://railway.app)
   - Create a new project
   - Select "Deploy from GitHub repo" or "Empty Project"

2. **Configure Environment Variables**
   In Railway dashboard, add:
   ```bash
   N8N_WEBHOOK_BASE_URL=https://your-n8n-url.com/webhook
   ```

3. **Deploy**
   - Railway will automatically detect the Dockerfile
   - Build and deploy will start automatically

4. **Access Your App**
   - Railway will provide a URL
   - The app will be available immediately after deployment

## Project Structure

```
streamlit-ui/
├── app.py                 # Main application (single file)
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── railway.json          # Railway deployment config
└── .gitignore           # Git ignore rules
```

## Configuration

Create a `.env` file in the `streamlit-ui` directory:

```env
N8N_WEBHOOK_BASE_URL=https://your-n8n-url.com/webhook
```

## License

Proprietary - All rights reserved
