# Scaler Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the scaler script
COPY . /app

# Install required packages
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN ls -l /app
# Command to run the scaler script
CMD ["python", "app.py"]
