# 🛡️ Honey Net: Self-Defending Digital Vault

An autonomous, agent-driven security system that uses LLMs (Gemini) to monitor, defend, and deceive intruders in a digital vault.

## 🚀 Deployment on Render

This project is configured for easy deployment on **Render**.

### Prerequisites
1. A [Render](https://render.com) account.
2. A GitHub repository containing this code.
3. A Google Gemini API Key.

### Steps to Deploy
1. **Push to GitHub**: Ensure all files (including `render.yaml` and `main.py`) are pushed to your GitHub repository.
2. **Create New Web Service**:
   - Go to the [Render Dashboard](https://dashboard.render.com).
   - Click **New +** and select **Web Service**.
   - Connect your GitHub repository.
3. **Configure Service**:
   - Render will automatically detect the `render.yaml` file and configure the service.
   - If not detected, use the following settings:
     - **Runtime**: `Python`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python main.py`
4. **Environment Variables**:
   - In the Render dashboard, go to the **Environment** tab.
   - Add a new variable:
     - Key: `GEMINI_API_KEY`
     - Value: `YOUR_ACTUAL_API_KEY_HERE`
5. **Deploy**: Click **Create Web Service**.

### How it works on Render
- The service runs `main.py`, which starts both the **Streamlit Dashboard** and the **Security Monitoring Sensor**.
- Streamlit will be accessible via the URL provided by Render (e.g., `https://honey-net.onrender.com`).
- **Note**: Since Render's filesystem is ephemeral, any files modified or restored will reset when the service restarts.

## 🛠️ Local Development
1. Install dependencies: `pip install -r requirements.txt`
2. Create a `.env` file with your `GEMINI_API_KEY`.
3. Run the system: `python main.py`
