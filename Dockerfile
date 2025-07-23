# Use official Python base image
FROM python:3.13-slim

# Set build argument for GitHub token
ARG GITHUB_TOKEN

# Combine all setup steps into a single RUN command to reduce layers
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        build-essential \
        pkg-config \
        libfreetype6-dev \
        libpng-dev \
        libxml2-dev \
        libxslt1-dev && \
    rm -rf /var/lib/apt/lists/* && \
    git clone https://${GITHUB_TOKEN}@github.com/plagye/polish_election_analysis_app.git /app && \
    cd /app && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /app/Dockerfile

# Set the working directory
WORKDIR /app

# Expose the port the app runs on
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]