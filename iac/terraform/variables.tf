variable "proxmox_endpoint" {
    type = string
    sensitive = true
}

variable "dev_root_password" {
    type = string
    sensitive = true
}

variable "dev_container_ip" {
    type = string
    sensitive = true
}

variable "ssh_keys" {
    type = string
    sensitive = true
}