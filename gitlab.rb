external_url 'http://172.21.86.168'  # Use the internal Docker service name
nginx['listen_port'] = 80
nginx['listen_https'] = false 
gitlab_rails['initial_root_password'] = "MySuperSecretAndSecurePassw0rd!"
