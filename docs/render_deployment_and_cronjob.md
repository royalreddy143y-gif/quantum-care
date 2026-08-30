# Separate Frontend & Backend Deployment Guide (Render)

This guide walks you through deploying **QuantumCare Frontend (React + Vite)** and **QuantumCare Backend (FastAPI)** as separate services on [Render](https://render.com) and connecting them using environment URLs.

---

## 🎯 Architecture Overview

```
 ┌────────────────────────────────────────┐          ┌────────────────────────────────────────┐
 │   Frontend Static Site (React + Vite)  │          │   Backend Web Service (FastAPI)        │
 │   https://quantumcare-frontend.onrender.com │ ──HTTP──► │   https://quantumcare-backend.onrender.com │
 └────────────────────────────────────────┘   (CORS) └────────────────────────────────────────┘
                    ▲                                                     ▲
                    │                                                     │
               Users Browser                                         Cron / Uptime
                                                                  (GET/HEAD /ping every 10m)
```

- **Frontend**: Render **Static Site** (100% Free, Global CDN, Instant Load, Zero Spin-Down).
- **Backend**: Render **Web Service** (Python 3.11 FastAPI).
- **Keep-Alive**: Pings `https://quantumcare-backend.onrender.com/ping` so the backend never spins down.

---

## 🚀 Step-by-Step Deployment Instructions

### Step 1: Deploy Backend API Service on Render

1. Log into your [Render Dashboard](https://dashboard.render.com).
2. Click **New +** → **Web Service**.
3. Connect your GitHub repository (`quantum-care`).
4. Configure the service settings:
   - **Name**: `quantumcare-backend`
   - **Region**: `Oregon (US West)` (or your preferred region)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `python run.py`
   - **Plan**: `Free`
5. Under **Advanced** → **Health Check Path**, enter: `/health`
6. Add the following **Environment Variables**:
   - `PYTHON_VERSION`: `3.11.8`
   - `ENVIRONMENT`: `production`
   - `MODEL_MODE`: `demo`
   - `PORT`: `10000`
   - `CORS_ORIGINS`: `*` (or your frontend Render URL once created)
   - `SECRET_KEY`: (Click *Generate* or provide a random 32+ char key)
7. Click **Create Web Service**.
8. Wait for the deploy to complete and copy your Backend URL:
   > Example: `https://quantumcare-backend.onrender.com`

---

### Step 2: Deploy Frontend Static Site on Render

1. In your [Render Dashboard](https://dashboard.render.com), click **New +** → **Static Site**.
2. Connect the same GitHub repository (`quantum-care`).
3. Configure the static site settings:
   - **Name**: `quantumcare-frontend`
   - **Branch**: `main`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
4. Under **Redirects / Rewrites**, add an SPA rewrite rule:
   - **Type**: `Rewrite`
   - **Source Path**: `/*`
   - **Destination Path**: `/index.html`
5. Add the **Environment Variable**:
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: `https://quantumcare-backend.onrender.com/api` *(replace with your actual backend URL + `/api`)*
6. Click **Create Static Site**.
7. Once deployed, open your frontend URL (`https://quantumcare-frontend.onrender.com`)!

---

### Step 3: (Optional) 1-Click Render Blueprint Deployment

If you prefer automated setup, Render can deploy both services together using [`render.yaml`](file:///e:/QuantumCare/render.yaml):

1. In Render Dashboard, click **New +** → **Blueprint**.
2. Select your repository. Render will automatically detect `render.yaml` and provision both:
   - `quantumcare-backend` (Web Service)
   - `quantumcare-frontend` (Static Site)
3. Click **Apply**.

---

## ⏰ Step 4: Configure Keep-Alive Cron Job (Prevents Backend Sleep)

Render Free web services spin down after 15 minutes of inactivity. Keep your backend awake 24/7 with any of these free options:

### Option A: Built-in GitHub Actions Workflow
In your GitHub repo:
1. Go to **Settings** → **Secrets and variables** → **Actions**.
2. Create repository secret `RENDER_APP_URL` = `https://quantumcare-backend.onrender.com`.
3. The included workflow ([`.github/workflows/render-keepalive.yml`](file:///e:/QuantumCare/.github/workflows/render-keepalive.yml)) will ping your backend `/ping` endpoint every 10 minutes automatically!

### Option B: cron-job.org (Free)
1. Sign up at [cron-job.org](https://cron-job.org).
2. Create Cronjob:
   - **URL**: `https://quantumcare-backend.onrender.com/ping`
   - **Schedule**: `Every 10 minutes`
   - **Method**: `GET` or `HEAD`

### Option C: UptimeRobot (Free Monitor)
1. Sign up at [UptimeRobot](https://uptimerobot.com).
2. Add Monitor:
   - **Type**: `HTTP(s)`
   - **URL**: `https://quantumcare-backend.onrender.com/health`
   - **Interval**: `5 minutes`

---

## 🔍 Verification Endpoints

Test your deployed backend directly:
- `https://quantumcare-backend.onrender.com/ping` → `{"status": "ok", "ping": "pong"}`
- `https://quantumcare-backend.onrender.com/health` → Status, DB connectivity, Uptime, ML Engine
- `https://quantumcare-backend.onrender.com/docs` → Interactive Swagger API documentation
