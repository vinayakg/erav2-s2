## Deployment

### Step1
`ssh -i ~/ab-yho.pem ubuntu@YOUR_EC2_PUBLIC_IP`

### Step 2: Install Dependencies on Ubuntu
````
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.12+ and essential tools
sudo apt install -y python3.12 python3.12-venv python3-pip curl git

# Install Tesseract OCR (required for your app)
sudo apt install -y tesseract-ocr tesseract-ocr-eng

# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
````

### Step 3: Clone Your GitHub Repository

`
git clone https://github.com/vinayakg/erav4-s2
`

`cd animal-file-upload`

`uv sync`

### Step 4: Test the Application

`uv run uvicorn main:app --host 0.0.0.0 --port 8000`


### Step 5: Setup fastapi as service
`sudo nano /etc/systemd/system/animal-app.service`

#### Paste this service configuration:

````
[Unit]
Description=Animal File Upload FastAPI App
After=network.target

[Service]
Type=exec
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/erav2-s2
Environment=PATH=/home/ubuntu/erav2-s2/.venv/bin
ExecStart=/home/ubuntu/erav2-s2/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
````

### Step 6: Start the Service
```
sudo systemctl daemon-reload
sudo systemctl enable animal-app
sudo systemctl start animal-app

# Check service status
sudo systemctl status animal-app
```

### Step 7: Install Caddy
```
# Install Caddy
sudo apt update
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy

# Check if Caddy is running
sudo systemctl status caddy
```

### Step 8: Create Caddyfile
```
sudo systemctl stop caddy

# Create Caddyfile
sudo nano /etc/caddy/Caddyfile

```

### Step 9: Start Services
```
bash# Start FastAPI service
sudo systemctl daemon-reload
sudo systemctl enable animal-app
sudo systemctl start animal-app

# Start Caddy
sudo systemctl enable caddy
sudo systemctl start caddy

# Check both services
sudo systemctl status animal-app
sudo systemctl status caddy
```

### Step 10: Caddy file for SSL

```
erav4-s2.vinayakg.dev {
    # Handle file uploads with larger size limit
    request_body {
        max_size 10MB
    }
    
    # Reverse proxy to FastAPI
    reverse_proxy localhost:8000
    
    # Optional: Add security headers
    header {
        # Security headers
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        X-Content-Type-Options nosniff
        X-Frame-Options DENY
        X-XSS-Protection "1; mode=block"
        Referrer-Policy strict-origin-when-cross-origin
    }
}

```