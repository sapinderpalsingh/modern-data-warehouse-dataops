/bin/bash -c "sudo echo \"${storage_account_name}${env}.blob.core.windows.net:/${storage_account_name}${env}/$container_name /$container_name nfs defaults,sec=sys,vers=3,nolock,proto=tcp,nofail 0 0\" >> /etc/fstab && sudo mkdir -p /$container_name && sudo apt-get update && sudo apt install -y nfs-common && mount /$container_name"