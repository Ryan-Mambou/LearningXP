provider "azurerm" {
  features {}
  
  # Azure credentials can be provided via:
  # 1. Environment variables: ARM_CLIENT_ID, ARM_CLIENT_SECRET, ARM_SUBSCRIPTION_ID, ARM_TENANT_ID
  # 2. Azure CLI: az login
  # 3. Service Principal (recommended for CI/CD)
}

