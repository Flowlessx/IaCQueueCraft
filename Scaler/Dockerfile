# Scaler Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the scaler script
COPY . /app
ENV PYTHONUNBUFFERED=0 
# Install required packages
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN ls -l /app
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

# Command to run the scaler script
CMD ["python","-u", "app.py"]
