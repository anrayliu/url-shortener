variable "proxmox_endpoint" {
  type      = string
  sensitive = true
}

variable "dev_root_password" {
  type      = string
  sensitive = true
}

variable "prod_root_password" {
  type      = string
  sensitive = true
}

variable "dev_container_ip" {
  type      = string
  sensitive = true
}

variable "prod_container_ip" {
  type      = string
  sensitive = true
}

variable "dev_ssh_keys" {
  type      = string
  sensitive = true
}

variable "prod_ssh_keys" {
  type      = string
  sensitive = true
}
