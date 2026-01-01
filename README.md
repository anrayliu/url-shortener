# DevOps Project: URL Shortener

Goal: Develop and deploy an app from scratch using a modern tech stack while touching every part of the product lifecycle.

## Features

- No "ClickOps". Infrastructure is managed as code with Terraform and Ansible.
- 3-tier application architecture that separates the web interface, REST API, and database.
- Isolated dev and prod environments. Changes are only applied to prod once merged into the main branch.
- On-prem system. Everything is ran on my bare-metal server.
- "Hybrid" CICD design. Combines modern GitHub Actions workflows with a local Jenkins server specifically for deployments. This design ultimately allows the online workflows to trigger deployments without exposing my intranet.
- Deploy the application for local testing with simple Docker Compose commands.

## Infrastructure Setup

While the application is loosely coupled and can be served as Docker images, the infrastructure setup is designed to fit
my own on-prem hardware. Requires a multibranch Jenkins job.

1. Create a `.env` file at repo root (see `.env.example` for help).
2. Generate 2 SSH key pairs for dev and prod root user with `ssh-keygen -t ed25519`.
3. Follow [these](https://github.com/Telmate/terraform-provider-proxmox/blob/master/docs/index.md) and [these](https://github.com/Telmate/terraform-provider-proxmox/blob/master/docs/guides/installation.md) to set up the Proxmox provider for Terraform.
4. Create `infrastructure/terraform/secrets.auto.tfvars` (see `infrastructure/terraform/tfvars.example` for help).
5. Run `terraform init`, `terraform plan` and `terraform apply`.
6. Create another SSH key pair for Jenkins.
7. Add the public key path to `vars` in `infrastructure/ansible/setup.yaml`.
8. Create `infrastructure/ansible/hosts` and add the dev and prod node IP addresses (see `hosts.example` for help).
9. Run `ansible-galaxy role install geerlingguy.docker`
10. Run `export PROD_HOST=x.x.x.x` and `export DEV_HOST=x.x.x.x`, replacing `x.x.x.x` with each respective host IP address.
11. Run ansible with `ansible-playbook setup.yaml -i hosts`