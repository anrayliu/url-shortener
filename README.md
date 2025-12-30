# url-shortener

Goal: develop and deploy an app from scratch using a modern tech stack while touching every part of the product lifecycle.


Infrastructure Setup:

Requires a running Jenkins server that polls your fork.

1. Create a `.env` file at repo root (see `.env.example` for help).
2. Generate 2 SSH key pairs for dev and prod root user with `ssh-keygen -t ed25519`.
3. Follow [these instructions](https://github.com/Telmate/terraform-provider-proxmox/blob/master/docs/guides/installation.md) to set up the Proxmox provider for Terraform
4. Create `infrastructure/terraform/secrets.auto.tfvars` and populate it like so:
```
proxmox_endpoint = "https://proxmox-endpoint:8006/api2/json"
dev_root_password = "root-password-for-dev"
dev_container_ip = "x.x.x.x/x"
prod_root_password = "root-password-for-prod"
prod_container_ip = "x.x.x.x/x"
dev_ssh_keys = <<-EOF
root-user-public-key-for-dev
EOF
prod_ssh_keys = <<-EOF
root-user-public-key-for-prod
EOF
```
5. Run `terraform init`, `terraform plan` and `terraform apply`.
6. Create another SSH key pair for Jenkins.
7. Add the public key path to `vars` in `infrastructure/ansible/setup.yaml`.
8. Create `infrastructure/ansible/hosts` and add the dev and prod node IP addresses.
9. Run `ansible-galaxy role install geerlingguy.docker`
10. Run ansible with `ansible-playbook setup.yaml -i hosts`
11. Add the IP addresses in Jenkins credentials as secret texts `dev-ip-addr` and `prod-ip-addr` respectively.
12. Create another set of credentials for the Jenkins user SSH named `jenkins-user`.
13. Go to [GitHub developer settings](https://github.com/settings/apps) and create a fine-grained PAT. Make sure it has read access to the repository "actions and metadata".
14. Add the PAT as a secret text credential named `github-pat`.