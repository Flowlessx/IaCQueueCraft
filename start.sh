sudo docker swarm leave  --force
sudo docker container prune
sudo docker compose build
sudo docker swarm init
sudo docker stack deploy -c docker-stack.yml tfself
sudo docker node inspect DESKTOP-BE2L4TD --format '{{ .Status.Addr }}'
sudo docker ps -a
