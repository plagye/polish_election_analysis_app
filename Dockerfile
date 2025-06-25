# Use official Python base image
FROM python:3.13-slim

# Set build argument for GitHub token
ARG GITHUB_TOKEN

# Install system dependencies
# - git: for cloning the repository
# - build-essential, pkg-config: for compiling C/C++ extensions
# - libfreetype6-dev, libpng-dev: specific libraries needed by Matplotlib for font and image handling
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    pkg-config \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Clone the private repository using the token
RUN git clone https://${GITHUB_TOKEN}@github.com/plagye/polish_election_analysis_app.git /app

# Set the working directory
WORKDIR /app

# Install Python dependencies
# This step is now more likely to succeed because the system dependencies are present.
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /app/Dockerfile

# Expose the port the app runs on
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]