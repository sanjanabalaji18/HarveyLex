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

1.  Go to your **Render Dashboard**.
2.  Click **New +** and select **Blueprint**.
3.  Connect your GitHub account and select the `harvey-lex` repository.
4.  Render will automatically detect the `render.yaml` file.
5.  **Crucial Step:** You will see a section called **"Environment Variables"** or **"Env Vars"** on the setup screen.
6.  It will ask for `GEMINI_API_KEY`.
7.  Paste your new API key there.
8.  Click **Apply** or **Create New Blueprint**.

## Step 3: Success!
Render will start building your Docker containers. This might take a few minutes.
Once finished, you will see a URL for your frontend (e.g., `https://harvey-lex-frontend.onrender.com`).

**That is your permanent link!**
