# Deployment Guide

## Prerequisites

1. AWS Account with appropriate permissions
2. Terraform installed (>= 1.0)
3. Ansible installed
4. SSH key pair for EC2 access
5. Polygon/Massive API key

## Step 1: Configure AWS Credentials

```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"
```

## Step 2: Set Up Terraform Variables

```bash
cd infrastructure/terraform
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` with your values:
- Set `key_name` to your SSH key pair name
- Set `db_username` and `db_password` for RDS
- Adjust `allowed_ssh_cidr` to your IP address

## Step 3: Provision Infrastructure

```bash
# Initialize Terraform
terraform init

# Review planned changes
terraform plan

# Apply infrastructure
terraform apply
```

Save the outputs:
```bash
terraform output app_public_ip
terraform output db_endpoint
```

## Step 4: Configure Ansible

```bash
cd ../ansible
cp inventory/production/hosts.example inventory/production/hosts
```

Edit `inventory/production/hosts` with:
- EC2 public IP from Terraform output
- RDS endpoint from Terraform output
- Database credentials
- Polygon API key

## Step 5: Deploy Application

```bash
# Test connectivity
ansible app_servers -m ping

# Deploy application
ansible-playbook -i inventory/production/hosts deploy.yml
```

## Step 6: Verify Deployment

```bash
# Check application health
curl http://YOUR_EC2_IP:8000/health

# View API documentation
open http://YOUR_EC2_IP:8000/docs
```

## Step 7: Populate Stock Data

```bash
# Populate Fortune 500 stocks
curl -X POST http://YOUR_EC2_IP:8000/api/v1/stocks/populate-fortune500
```

## CI/CD with GitHub Actions

### Required Secrets

Configure these secrets in your GitHub repository:

1. `AWS_ACCESS_KEY_ID`: AWS access key
2. `AWS_SECRET_ACCESS_KEY`: AWS secret key
3. `AWS_REGION`: AWS region (e.g., us-east-1)
4. `DB_USERNAME`: Database username
5. `DB_PASSWORD`: Database password
6. `SSH_KEY_NAME`: SSH key pair name
7. `SSH_PRIVATE_KEY`: Contents of your SSH private key
8. `POLYGON_API_KEY`: Polygon/Massive API key

### Automated Deployment

Push to `main` branch triggers automatic deployment:

```bash
git push origin main
```

## Database Migrations

Migrations run automatically during deployment. To run manually:

```bash
ssh -i ~/.ssh/portfolio-api-key.pem ec2-user@YOUR_EC2_IP
cd /opt/portfolio-api
alembic upgrade head
```

## Monitoring

### Application Logs

```bash
# View application logs
ssh -i ~/.ssh/portfolio-api-key.pem ec2-user@YOUR_EC2_IP
sudo journalctl -u portfolio-api -f
```

### Prometheus Metrics

Access metrics at: `http://YOUR_EC2_IP:8000/metrics`

## Rollback

To rollback to a previous version:

```bash
cd infrastructure/ansible
ansible-playbook -i inventory/production/hosts deploy.yml -e "branch=PREVIOUS_COMMIT_SHA"
```

## Teardown

To destroy all infrastructure:

```bash
cd infrastructure/terraform
terraform destroy
```

## Troubleshooting

### Application won't start

Check logs:
```bash
sudo journalctl -u portfolio-api -n 50
```

### Database connection issues

Verify security group allows EC2 to connect to RDS:
```bash
telnet YOUR_RDS_ENDPOINT 5432
```

### Terraform state locked

If Terraform state is locked, manually unlock:
```bash
terraform force-unlock LOCK_ID
```
