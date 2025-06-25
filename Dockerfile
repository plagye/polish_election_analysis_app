# Use official Python base image
FROM python:3.11-slim

# Set build argument for GitHub token
ARG GITHUB_TOKEN

# Install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Clone the private repository using the token
RUN git clone https://$GITHUB_TOKEN@github.com/plagye/polish_election_analysis_app.git /app

WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /app/Dockerfile

# Expose the port the app runs on
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]
