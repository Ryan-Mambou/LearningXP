# Guide Simple - Déploiement sur Azure

Ce guide explique comment déployer l'application sur une VM Azure de manière simple.

## 📋 Ce que fait Terraform

Terraform crée automatiquement :
1. ✅ Un groupe de ressources Azure
2. ✅ Une machine virtuelle Ubuntu
3. ✅ Un réseau virtuel et une adresse IP publique
4. ✅ Un firewall (groupe de sécurité)
5. ✅ Déploie votre application Flask

## 🚀 Démarrage Rapide

### Étape 1: Installer Terraform

```bash
# macOS
brew install terraform

# Windows
# Téléchargez depuis https://www.terraform.io/downloads
```

### Étape 2: Se connecter à Azure

```bash
az login
```

### Étape 3: Générer une clé SSH

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
```

**Important**: Ne mettez PAS de mot de passe (appuyez juste sur Entrée).

### Étape 4: Configurer Terraform

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Ouvrez `terraform.tfvars` et ajoutez votre clé SSH publique :

```hcl
ssh_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC... votre-clé-ici"
```

Pour obtenir votre clé publique :
```bash
cat ~/.ssh/id_rsa.pub
```

### Étape 5: Déployer

```bash
terraform init
terraform plan   # Voir ce qui sera créé
terraform apply   # Créer la VM et déployer l'application
```

C'est tout ! 🎉

## 🔑 Secrets GitHub (pour CI/CD)

Pour que GitHub Actions déploie automatiquement, ajoutez **un seul secret** :

### Secret: `AZURE_CREDENTIALS`

**Comment créer :**

```bash
az ad sp create-for-rbac --name "github-actions-learningxp" \
  --role="Contributor" \
  --scopes="/subscriptions/VOTRE_SUBSCRIPTION_ID" \
  --sdk-auth
```

**Copiez le JSON complet** et ajoutez-le comme secret `AZURE_CREDENTIALS` dans GitHub :
- Settings → Secrets and variables → Actions → New repository secret

**Format du JSON :**
```json
{
  "clientId": "xxx",
  "clientSecret": "xxx",
  "subscriptionId": "xxx",
  "tenantId": "xxx"
}
```

## 📝 Variables

| Variable | Description | Défaut |
|----------|-------------|--------|
| `ssh_public_key` | Votre clé SSH publique | **Obligatoire** |
| `resource_group_name` | Nom du groupe Azure | `learningxp-rg` |
| `location` | Région Azure | `West Europe` |

## 🔍 Vérifier le déploiement

Après `terraform apply`, vous verrez :
- L'adresse IP de la VM
- L'URL de l'application

Testez l'application :
```bash
curl http://ADRESSE_IP:5000/api/health
```

## 🗑️ Supprimer les ressources

Pour supprimer la VM et économiser de l'argent :
```bash
terraform destroy
```

## ❓ Questions Fréquentes

**Q: Combien ça coûte ?**  
A: Environ 15-20€/mois pour une VM Standard_B2s.

**Q: Comment me connecter à la VM ?**  
A: `ssh -i ~/.ssh/id_rsa azureuser@ADRESSE_IP`

**Q: Où est l'application ?**  
A: Dans `/opt/learningxp` sur la VM.

**Q: Comment mettre à jour l'application ?**  
A: Modifiez `app.py`, puis `terraform apply` - Terraform détecte les changements automatiquement.
