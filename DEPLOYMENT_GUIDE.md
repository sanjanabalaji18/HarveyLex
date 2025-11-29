# Deployment Guide for Render.com

Follow these steps to get your application online with a permanent link.

## Prerequisites
1.  **GitHub Account**: You need a GitHub account.
2.  **Render Account**: Sign up at [render.com](https://render.com) (you can log in with GitHub).

## Step 1: Push Code to GitHub
You need to put your code in a GitHub repository.

1.  Create a new repository on GitHub (e.g., `harvey-lex`).
2.  Run these commands in your terminal:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/harvey-lex.git
git push -u origin main
```
*(Replace `<YOUR_USERNAME>` with your actual GitHub username)*

## Step 2: Deploy on Render

### Option A: Using Blueprint (Recommended)
1.  Go to your **Render Dashboard**.
2.  Click **New +** and select **Blueprint**.
3.  Connect your GitHub account and select the `harvey-lex` repository.
4.  Render will automatically detect the `render.yaml` file.
    *   *Note: We have configured `render.yaml` to build the backend from the `backend/` directory.*
5.  **Environment Variables**: You will be prompted for `GEMINI_API_KEY`. Paste your API key here.
6.  Click **Apply** or **Create New Blueprint**.

### Option B: Manual Setup (Web Service)
If you prefer to set up the Backend manually:
1.  Create a new **Web Service**.
2.  Connect your repo.
3.  **Runtime**: Docker.
4.  **Root Directory**: `backend` (This is critical!).
5.  **Build Context**: `.` (Default, relative to Root Directory).
6.  **Dockerfile Path**: `Dockerfile` (Default).
7.  Add Environment Variable: `GEMINI_API_KEY`.

### Option C: Manual Setup (Frontend)
If you need to set up the Frontend manually:
1.  Create a new **Web Service**.
2.  Connect your repo.
3.  **Runtime**: Docker.
4.  **Root Directory**: `frontend/app` (This is critical!).
5.  **Build Context**: `.` (Default, relative to Root Directory).
6.  **Dockerfile Path**: `Dockerfile` (Default).
7.  Add Environment Variable: `VITE_API_URL` -> `https://<YOUR_BACKEND_URL>.onrender.com`.

## Step 3: Success!
Render will start building your Docker containers. This might take a few minutes.
Once finished, you will see a URL for your frontend (e.g., `https://harvey-lex-frontend.onrender.com`).

**That is your permanent link!**
