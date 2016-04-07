# -*- mode: ruby -*-
# vi: set ft=ruby :

TIMTEC_USER = "vagrant"

$runserver = <<SCRIPT
    # must run with vagrant user
    # cd /vagrant
    cd /home/vagrant/timtec
    ~/env/bin/python manage.py migrate

    tmux -2 new-session -d -s vagrant -n 'django'
    tmux send-keys "/home/vagrant/env/bin/python manage.py runserver 0.0.0.0:8000" C-m

SCRIPT

Vagrant.configure('2') do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision :shell, path: "scripts/bootstrap-ubuntu.sh", privileged: false, keep_color: true
  # config.vm.provision :shell, path: "scripts/production-ubuntu.sh", privileged: false, keep_color: true
  config.vm.provision "shell",
           inline: $runserver,
           privileged: false,
           run: "always"
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.ssh.username = TIMTEC_USER
  config.vm.synced_folder "./", "/home/" + TIMTEC_USER  + "/timtec/", create: true
end
