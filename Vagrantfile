# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  config.vm.box = "ubuntu/bionic64"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  config.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # config.vm.provider "virtualbox" do |vb|
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    set -e

    apt-get update && apt-get install -y python3-pip
    pip3 install -U pip
    pip3 install -r /vagrant/requirements.txt
    ln -sf /usr/bin/python3 /usr/bin/python
    grep --silent PYTHONDONTWRITEBYTECODE /home/vagrant/.profile || echo "export PYTHONDONTWRITEBYTECODE=1" >> /home/vagrant/.profile
    grep --silent vagrant /home/vagrant/.profile || echo "cd /vagrant" >> /home/vagrant/.profile
  SHELL
end
