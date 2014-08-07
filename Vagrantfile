Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/precise32"
  config.vm.provider "virtualbox" do |v|
	v.gui = true
  end
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, '--audio', 'coreaudio', '--audiocontroller', 'hda'] # choices: hda sb16 ac97
  end
  config.vm.provision "shell", path: "vagrantbootstrap.sh"
end
