# Fichiers de l'application à déployer
data "local_file" "app_py" {
  filename = "${path.module}/../app.py"
}

data "local_file" "requirements" {
  filename = "${path.module}/../requirements.txt"
}

# Déploiement de l'application sur la VM
resource "null_resource" "deploy_app" {
  # Redéployer si les fichiers changent
  triggers = {
    app_py_hash       = data.local_file.app_py.content_base64sha256
    requirements_hash = data.local_file.requirements.content_base64sha256
    vm_id             = azurerm_linux_virtual_machine.main.id
  }

  # Connexion SSH à la VM
  connection {
    type        = "ssh"
    host        = azurerm_public_ip.main.ip_address
    user        = "azureuser"
    private_key = file("${pathexpand("~")}/.ssh/azure_learningxp")
    timeout     = "5m"
  }

  # Étape 1: Créer le dossier de l'application
  provisioner "remote-exec" {
    inline = [
      "sudo mkdir -p /opt/learningxp",
      "sudo chown azureuser:azureuser /opt/learningxp"
    ]
  }

  # Étape 2: Copier les fichiers de l'application
  provisioner "file" {
    source      = "${path.module}/../app.py"
    destination = "/opt/learningxp/app.py"
  }

  provisioner "file" {
    source      = "${path.module}/../requirements.txt"
    destination = "/opt/learningxp/requirements.txt"
  }

  # Étape 3: Installer Python et les dépendances
  provisioner "remote-exec" {
    inline = [
      "cd /opt/learningxp",
      # Créer l'environnement virtuel Python
      "if [ ! -d 'venv' ]; then python3 -m venv venv; fi",
      # Activer et installer les dépendances
      "source venv/bin/activate",
      "pip install --upgrade pip",
      "pip install -r requirements.txt"
    ]
  }

  # Étape 4: Créer le service systemd pour démarrer l'application automatiquement
  provisioner "remote-exec" {
    inline = [
      "sudo tee /etc/systemd/system/learningxp.service > /dev/null << 'EOF'",
      "[Unit]",
      "Description=LearningXP Flask Application",
      "After=network.target",
      "",
      "[Service]",
      "Type=simple",
      "User=azureuser",
      "WorkingDirectory=/opt/learningxp",
      "Environment='PATH=/opt/learningxp/venv/bin'",
      "ExecStart=/opt/learningxp/venv/bin/python /opt/learningxp/app.py",
      "Restart=always",
      "RestartSec=10",
      "",
      "[Install]",
      "WantedBy=multi-user.target",
      "EOF",
      # Recharger systemd et démarrer le service
      "sudo systemctl daemon-reload",
      "sudo systemctl enable learningxp",
      "sudo systemctl restart learningxp"
    ]
  }

  depends_on = [azurerm_linux_virtual_machine.main]
}
