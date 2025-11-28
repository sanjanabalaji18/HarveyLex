# How to Share Your Website

Since your application is running locally on your computer, other people cannot access it directly. To share it, you need to expose your local server to the internet.

## Option 1: Temporary Sharing (Easiest)
Use this method to quickly show your work to someone for a demo. It creates a temporary public URL that tunnels to your computer.

### Method A: Using SSH (No installation required)
Run this command in your terminal:

```bash
ssh -R 80:localhost:5173 serveo.net
```
**Or**
```bash
ssh -R 80:localhost:5173 nokey@localhost.run
```

- The terminal will print a URL (e.g., `https://random-name.serveo.net`).
- Share this URL with anyone.
- **Note:** The link stops working when you close the terminal or stop the command (Ctrl+C).

### Method B: Using Ngrok (More stable)
1. Download and install [ngrok](https://ngrok.com/download).
2. Run: `ngrok http 5173`
3. Copy the `https://...` forwarding URL.

## Option 2: Permanent Deployment (Professional)
Use this method if you want the website to be always available, even when your computer is off.

### Recommended Platforms
Since your project is Dockerized, you can deploy it easily to platforms that support Docker:

1.  **Render / Railway / Fly.io**
    - Push your code to GitHub.
    - Connect your repository to the service.
    - They will build your Dockerfile and host it.

2.  **DigitalOcean / AWS / Google Cloud**
    - Rent a virtual server (VPS).
    - Install Docker on it.
    - Run your `deploy.sh` script on that server.
