Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/precise32"
  config.vm.provider "virtualbox" do |v|
	v.gui = true
  end
  config.vm.provision "shell", path: "vagrantbootstrap.sh"
end
