# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install systemd
RUN apt-get update && apt-get install -y git

# Switch to root user to set ulimit
USER root

# Increase file descriptor limits
RUN ulimit -n 65536

# Switch back to non-root user
USER nobody

# Expose port 5000 for the Flask app
EXPOSE 5001
ENV BACKEND_HOST=http://backend
ENV BACKEND_PORT=5000
# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
