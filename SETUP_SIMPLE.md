# 🚀 Guide Simple - Déploiement Azure

Guide ultra-simple pour déployer votre application Flask sur Azure.

## 📝 Ce dont vous avez besoin

1. Un compte Azure (gratuit avec crédit de départ)
2. Azure CLI installé (`az`)
3. Terraform installé
4. Une clé SSH

## ⚡ Déploiement en 5 étapes

### Étape 1: Installer les outils

```bash
# Installer Azure CLI
# macOS:
brew install azure-cli

# Installer Terraform
brew install terraform
```

### Étape 2: Se connecter à Azure

```bash
az login
```

Ouvrez le navigateur et connectez-vous.

### Étape 3: Créer une clé SSH

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
```

**Important**: Appuyez juste sur Entrée (pas de mot de passe).

### Étape 4: Configurer Terraform

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Ouvrez `terraform.tfvars` et ajoutez votre clé SSH :

```hcl
ssh_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC... votre-clé-ici"
```

Pour obtenir votre clé :

```bash
cat ~/.ssh/id_rsa.pub
```

### Étape 5: Déployer !

```bash
terraform init
terraform apply
```

Tapez `yes` quand demandé.

**C'est tout !** 🎉 Votre application est déployée !

## 🔑 Pour GitHub Actions (automatique)

Pour que GitHub déploie automatiquement après chaque merge :

1. Créez un Service Principal Azure :

```bash
az ad sp create-for-rbac --name "github-actions-learningxp" \
  --role="Contributor" \
  --scopes="/subscriptions/VOTRE_SUBSCRIPTION_ID" \
  --sdk-auth
```

2. Copiez le JSON qui s'affiche

3. Dans GitHub :

   - **Settings** → **Secrets** → **Actions**
   - **New repository secret**
   - Nom: `AZURE_CREDENTIALS`
   - Valeur: Collez le JSON

4. Mergez sur `main` → Déploiement automatique ! ✨

## 📊 Résumé

**Localement:**

- `terraform apply` → Crée la VM et déploie

**GitHub Actions:**

- Merge sur `main` → Déploie automatiquement

**Un seul secret GitHub:**

- `AZURE_CREDENTIALS` (JSON du Service Principal)

## 💰 Coûts

- VM Standard_B2s: ~15-20€/mois
- Pour économiser: `terraform destroy` quand vous n'en avez pas besoin

## ❓ Besoin d'aide ?

- Voir l'IP de la VM: `terraform output`
- Se connecter: `ssh -i ~/.ssh/id_rsa azureuser@IP`
- Tester l'app: `curl http://IP:5000/api/health`
