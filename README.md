# url-shortener

Goal: develop and deploy an app from scratch using a modern tech stack while touching every part of the product lifecycle.

Infrastructure Setup (dev environment):

Requires a running Jenkins server that polls this repo.

1. Create a `.env` file at repo root (see `.env.example` for help).
2. Generate an SSH key pair for root user with `ssh-keygen -t ed25519`.
3. Follow [these instructions](https://github.com/Telmate/terraform-provider-proxmox/blob/master/docs/guides/installation.md) to set up the Proxmox provider for Terraform
4. Create `infrastructure/terraform/secrets.auto.tfvars` and populate it like so:
```
proxmox_endpoint = "https://proxmox-endpoint:8006/api2/json"
dev_root_password = "root-password"
dev_container_ip = "x.x.x.x/x"
ssh_keys = <<-EOF
root-user-public-key
EOF
```
4. Run `terraform init`, `terraform plan` and `terraform apply`.
5. Create another SSH key pair for a Jenkins user.
6. Add the public key path to `vars` in `infrastructure/ansible/setup.yaml`.
7. Create `infrastructure/ansible/hosts` and add the node ip address to it.
8. Run `ansible-galaxy role install geerlingguy.docker`
9. Run ansible with `ansible-playbook setup.yaml -i hosts`
10. Add ip addresses to Jenkins credentials.