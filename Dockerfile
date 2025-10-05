# ---------- Flask Beats Dockerfile ----------
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for SoX)
RUN apt-get update && apt-get install -y sox libsox-fmt-all && rm -rf /var/lib/apt/lists/*

# Copy app files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Default to dev mode (can override in docker-compose)
ENV FLASK_ENV=development

# Run app
CMD ["python3", "app.py"]
