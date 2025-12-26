# url-shortener

Goal: develop and deploy an app from scratch using a modern tech stack while touching every part of the product lifecycle.

Infrastructure Setup (dev environment):

1. Create a `.env` file at repo root (see `.env.example` for help)
2. Generate an SSH key pair for root user. 
3. Create `iac/terraform/secrets.auto.tfvars` and populate it like so:
```
proxmox_endpoint = "https://proxmox-endpoint:8006/api2/json"
dev_root_password = "root-password"
dev_container_ip = "x.x.x.x/x"

ssh_keys = <<-EOF
root-user-public-key
EOF
```
4. Run terraform.
5. Create another SSH key pair for jenkins user.
6. Add the public key path to `iac/ansible/setup.yaml`.
7. Create `iac/ansible/hosts` and add the node ip address to it.
8. Run `ansible-galaxy role install geerlingguy.docker`
9. Run ansible.