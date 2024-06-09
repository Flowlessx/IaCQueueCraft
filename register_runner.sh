#!/bin/sh

# Wait for GitLab to be ready
until curl -sSf http://172.21.86.168/; do
  echo "Waiting for GitLab to be ready..."
  sleep 5
done

# Retrieve registration token
TOKEN=$(curl -sSf --header "PRIVATE-TOKEN: $(cat /run/secrets/gitlab_root_password)" \
  http://172.21.86.168/api/v4/runners | jq -r .token)

# Register GitLab runner
sudo gitlab-runner register --url http://172.21.86.168/ --registration-token $token