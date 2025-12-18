# Secrets GitHub - Guide Simple

Pour déployer automatiquement sur Azure et pousser des images Docker, vous avez besoin de **3 secrets** :

## 🔑 Secrets Obligatoires

### 1. `AZURE_CREDENTIALS`

Contient les informations pour se connecter à Azure.

**Comment créer :**

1. Connectez-vous à Azure :

```bash
az login
```

2. Créez un Service Principal :

```bash
az ad sp create-for-rbac --name "github-actions-learningxp" \
  --role="Contributor" \
  --scopes="/subscriptions/VOTRE_SUBSCRIPTION_ID" \
  --sdk-auth
```

3. **Copiez tout le JSON** qui s'affiche

4. Dans GitHub :
   - Allez dans **Settings** → **Secrets and variables** → **Actions**
   - Cliquez sur **New repository secret**
   - Nom : `AZURE_CREDENTIALS`
   - Valeur : Collez le JSON complet

**Exemple de JSON :**

```json
{
  "clientId": "12345678-1234-1234-1234-123456789012",
  "clientSecret": "abcdefghijklmnopqrstuvwxyz123456",
  "subscriptionId": "87654321-4321-4321-4321-210987654321",
  "tenantId": "11111111-2222-3333-4444-555555555555"
}
```

### 2. `DOCKER_HUB_USERNAME`

Votre nom d'utilisateur Docker Hub.

**Comment créer :**

1. Allez sur https://hub.docker.com
2. Créez un compte si vous n'en avez pas
3. Notez votre nom d'utilisateur

**Dans GitHub :**

- Allez dans **Settings** → **Secrets and variables** → **Actions**
- Cliquez sur **New repository secret**
- Nom : `DOCKER_HUB_USERNAME`
- Valeur : Votre nom d'utilisateur Docker Hub (ex: `monusername`)

### 3. `DOCKER_HUB_TOKEN`

**⚠️ IMPORTANT :** Vous devez créer un **Access Token**, pas utiliser votre mot de passe !

**Comment créer un token avec les bonnes permissions :**

1. Allez sur https://hub.docker.com/settings/security
2. Cliquez sur **New Access Token**
3. **Nom du token** : `github-actions-learningxp` (ou n'importe quel nom)
4. **Permissions** : Sélectionnez **Read & Write** (ou au minimum **Read, Write & Delete**)
5. Cliquez sur **Generate**
6. **⚠️ IMPORTANT :** Copiez le token immédiatement (vous ne pourrez plus le voir après)

**Dans GitHub :**

- Allez dans **Settings** → **Secrets and variables** → **Actions**
- Cliquez sur **New repository secret**
- Nom : `DOCKER_HUB_TOKEN`
- Valeur : Collez le token que vous venez de copier

**⚠️ Note importante :**

- Le token doit avoir les permissions **Read & Write** pour pouvoir pousser des images
- Si vous avez une erreur "insufficient scopes", supprimez l'ancien token et créez-en un nouveau avec les bonnes permissions

## ✅ C'est tout !

Une fois ces secrets ajoutés, GitHub Actions pourra :

- ✅ Se connecter à Azure
- ✅ Créer la VM automatiquement
- ✅ Déployer votre application
- ✅ Construire et pousser l'image Docker vers Docker Hub

## 🔍 Comment trouver votre Subscription ID

```bash
az account show --query id -o tsv
```

Ou dans le portail Azure : **Subscriptions** → Copiez l'ID de votre abonnement
