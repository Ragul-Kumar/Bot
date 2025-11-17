FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Optional: install ffmpeg for compression (remove if not needed)
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
 && rm -rf /var/lib/apt/lists/*

# Upgrade pip first (helps avoid build issues)
RUN python -m pip install --upgrade pip setuptools wheel

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Create and use non-root user
RUN useradd --create-home appuser
USER appuser
WORKDIR /home/appuser
COPY --chown=appuser:appuser . /home/appuser

CMD ["python", "bot.py"]
