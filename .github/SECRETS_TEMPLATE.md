# Secrets GitHub - Guide Simple

Pour déployer automatiquement sur Azure, vous avez besoin d'**un seul secret** :

## 🔑 Secret Obligatoire

### `AZURE_CREDENTIALS`

C'est le seul secret nécessaire ! Il contient les informations pour se connecter à Azure.

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

## ✅ C'est tout !

Une fois ce secret ajouté, GitHub Actions pourra :
- ✅ Se connecter à Azure
- ✅ Créer la VM automatiquement
- ✅ Déployer votre application

## 🔍 Comment trouver votre Subscription ID

```bash
az account show --query id -o tsv
```

Ou dans le portail Azure : **Subscriptions** → Copiez l'ID de votre abonnement
