# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN ls -l /app
# Define environment variable
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV DB_USER=root
ENV DB_PASSWORD=root
ENV DB_HOST=postgres
ENV DB_NAME=root
ENV Gitlab_Token=glpat-BWPnFeRJxzCum47VRUaV
CMD ["python", "-u", "app.py"]
