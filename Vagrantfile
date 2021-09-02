# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure("2") do |config|
  
    config.vm.box = "ubuntu/bionic64"
    config.vm.hostname = "foilv"
    config.vm.network :private_network, ip: "192.168.3.223"

  
    config.vm.provider "virtualbox" do |v|
      v.memory = 6144
      v.cpus = 4
    end
  
    config.vm.provision "ansible" do |ansible|    
      ansible.playbook = "playbook.yml"
      
    end
  
  end
  