# -*- mode: ruby -*-
# vi: set ft=ruby :

TIMTEC_USER = "vagrant"

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision :shell, path: "scripts/bootstrap-ubuntu.sh", privileged: false, keep_color: true
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.ssh.username = TIMTEC_USER
  config.vm.synced_folder "./", "/home/" + TIMTEC_USER  + "/timtec/", create: true
end
