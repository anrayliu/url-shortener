terraform {
  required_providers {
    proxmox = {
      source  = "telmate/proxmox"
      version = "3.0.2-rc07"
    }
  }
}

provider "proxmox" {
  pm_api_url = var.proxmox_endpoint
  pm_tls_insecure = true
}

resource "proxmox_lxc" "dev" {
    features {
        nesting = true
    }
    ssh_public_keys = var.ssh_keys
    hostname = "url-shortener-dev"
    network {
        name = "eth0"
        bridge = "vmbr0"
        ip = "dhcp"
    }
    rootfs {
        storage = "local-lvm"
        size    = "4G"
    }
    ostemplate = "local:vztmpl/ubuntu-24.04-standard_24.04-2_amd64.tar.zst"
    cores = 1
    memory = 3072
    onboot = true
    start = true
    password = var.dev_root_password
    target_node = "pve"
    unprivileged = true
}
