FROM python:3.8-slim

# Install Python dependencies
RUN pip install rq-dashboard

ENTRYPOINT ["/bin/bash", "-c", "rq-dashboard -H redis"]