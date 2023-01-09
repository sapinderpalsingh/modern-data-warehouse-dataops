variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Loaction where the resources are to be deployed"
  type        = string
}

variable "acr_name" {
  description = "Name of the Azure Container Registry"
  type        = string
}

variable "batch_uami_id" {
  type        = string
  description = "Managed identity ID"
}

variable "acr_sku" {
  description = "value"
  type        = string
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
}
