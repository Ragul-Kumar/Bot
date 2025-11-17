# Bot

A simple Python bot project with Docker support and required video assets.  
This repository contains the bot script, Docker configuration, and video files used by the application.

---

## 📦 Requirements

- Python 3.8+
- pip  
- Docker & Docker Compose (optional)  
- (Optional) Git LFS for large video files  

### Install Python Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🚀 Local Setup

### Clone the repository

```bash
git clone https://github.com/Ragul-Kumar/Bot.git
cd Bot
```

### (Optional) Remove tracked virtual environment

```bash
git rm -r --cached venv
echo "venv/" >> .gitignore
git add .gitignore
git commit -m "Ignore venv"
```

### Run the bot

```bash
python bot.py
```

---

## 🐳 Run with Docker

### Build the Docker image

```bash
docker build -t bot-app .
```

### Run the container

```bash
docker run --rm -it \
  -v "$(pwd)/videos:/app/videos" \
  bot-app
```

### Using Docker Compose

```bash
docker-compose up --build
```

---

## 🧪 Usage

Modify this based on your bot logic.

### Example (local)

```bash
python bot.py --input videos/video1.mp4
```

### Example (Docker)

```bash
docker run -v "$(pwd)/videos:/app/videos" bot-app --input /app/videos/video1.mp4
```

---

## 📝 Deployment Notes

- Video files **must remain included** for correct deployment.  
- For large files, consider **Git LFS**.  
- Docker can mount videos from local storage for better performance.

---

## 📦 Large File Best Practices

### Use Git LFS for videos

```bash
git lfs install
git lfs track "*.mp4"
git add .gitattributes
git add *.mp4
git commit -m "Move video files to Git LFS"
git push
```

### Keep virtual environment out of Git

```bash
git rm -r --cached venv
echo "venv/" >> .gitignore
```

---

## 📁 Project Structure

```
├─ venv/                  # Virtual environment (should be ignored)
├─ bot.py                 # Main bot script
├─ Dockerfile             # Docker image build
├─ docker-compose.yml     # Docker Compose configuration
├─ requirements.txt       # Python dependencies
├─ video1.mp4             # Video asset
├─ video2.mp4             # Video asset
├─ video3.mp4             # Video asset
└─ .gitignore             # Git ignore rules
```

## 📧 Contact

Maintained by **Ragul Kumar**  
GitHub: https://github.com/Ragul-Kumar
