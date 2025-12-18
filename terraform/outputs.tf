# Sorties après le déploiement

output "vm_public_ip" {
  description = "Adresse IP publique de la VM"
  value       = azurerm_public_ip.main.ip_address
}

output "app_url" {
  description = "URL pour accéder à l'application"
  value       = "http://${azurerm_public_ip.main.ip_address}:5000"
}

output "ssh_command" {
  description = "Commande pour se connecter à la VM"
  value       = "ssh -i ~/.ssh/azure_learningxp azureuser@${azurerm_public_ip.main.ip_address}"
}
