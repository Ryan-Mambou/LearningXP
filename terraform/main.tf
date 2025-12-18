# Groupe de ressources Azure
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

# Réseau virtuel
resource "azurerm_virtual_network" "main" {
  name                = "learningxp-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

# Sous-réseau
resource "azurerm_subnet" "main" {
  name                 = "learningxp-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Adresse IP publique
resource "azurerm_public_ip" "main" {
  name                = "learningxp-public-ip"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  allocation_method   = "Static"
}

# Groupe de sécurité réseau (firewall)
resource "azurerm_network_security_group" "main" {
  name                = "learningxp-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  # Autoriser SSH (port 22)
  security_rule {
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Autoriser HTTP (port 80)
  security_rule {
    name                       = "HTTP"
    priority                   = 1002
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Autoriser l'application Flask (port 5000)
  security_rule {
    name                       = "FlaskApp"
    priority                   = 1003
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "5000"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

# Interface réseau
resource "azurerm_network_interface" "main" {
  name                = "learningxp-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.main.id
  }
}

# Associer le groupe de sécurité au réseau
resource "azurerm_network_interface_security_group_association" "main" {
  network_interface_id      = azurerm_network_interface.main.id
  network_security_group_id = azurerm_network_security_group.main.id
}

# Machine virtuelle Linux Ubuntu
resource "azurerm_linux_virtual_machine" "main" {
  name                = "learningxp-vm"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  size                = "Standard_B2s"  # 2 CPU, 4 GB RAM
  admin_username      = "azureuser"

  network_interface_ids = [
    azurerm_network_interface.main.id,
  ]

  # Clé SSH pour se connecter à la VM
  admin_ssh_key {
    username   = "azureuser"
    public_key = var.ssh_public_key
  }

  # Disque système
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  # Image Ubuntu
  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  # Script d'initialisation (installe Python, etc.)
  custom_data = base64encode(file("${path.module}/cloud-init.yml"))
}
