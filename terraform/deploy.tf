# Fichiers de l'application à déployer
data "local_file" "server_py" {
  filename = "${path.module}/../server.py"
}

data "local_file" "index_html" {
  filename = "${path.module}/../index.html"
}

data "local_file" "requirements" {
  filename = "${path.module}/../requirements.txt"
}

# Déploiement de l'application sur la VM
resource "null_resource" "deploy_app" {
  # Redéployer si les fichiers changent
  triggers = {
    server_py_hash    = data.local_file.server_py.content_base64sha256
    index_html_hash   = data.local_file.index_html.content_base64sha256
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
    source      = "${path.module}/../server.py"
    destination = "/opt/learningxp/server.py"
  }

  provisioner "file" {
    source      = "${path.module}/../index.html"
    destination = "/opt/learningxp/index.html"
  }

  provisioner "file" {
    source      = "${path.module}/../requirements.txt"
    destination = "/opt/learningxp/requirements.txt"
  }

  # Copier le dossier static
  provisioner "remote-exec" {
    inline = [
      "mkdir -p /opt/learningxp/static/css /opt/learningxp/static/js"
    ]
  }

  provisioner "file" {
    source      = "${path.module}/../static/css/style.css"
    destination = "/opt/learningxp/static/css/style.css"
  }

  provisioner "file" {
    source      = "${path.module}/../static/js/app.js"
    destination = "/opt/learningxp/static/js/app.js"
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
      "Description=LearningXP Web Application",
      "After=network.target",
      "",
      "[Service]",
      "Type=simple",
      "User=azureuser",
      "WorkingDirectory=/opt/learningxp",
      "Environment='PATH=/opt/learningxp/venv/bin'",
      "ExecStart=/opt/learningxp/venv/bin/python /opt/learningxp/server.py",
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
