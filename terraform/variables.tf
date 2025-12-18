# Variables simples pour la configuration Azure

variable "ssh_public_key" {
  description = "Votre clé SSH publique (générée avec: ssh-keygen -t rsa -b 4096)"
  type        = string
}

variable "resource_group_name" {
  description = "Nom du groupe de ressources Azure"
  type        = string
  default     = "learningxp-rg"
}

variable "location" {
  description = "Région Azure (ex: West Europe, France Central)"
  type        = string
  default     = "West Europe"
}
