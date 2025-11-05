# Terraform outputs.

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = module.vpc.private_subnet_ids
}

output "db_endpoint" {
  description = "RDS endpoint"
  value       = module.rds.db_endpoint
  sensitive   = true
}

output "db_name" {
  description = "Database name"
  value       = var.db_name
}

output "app_instance_id" {
  description = "EC2 instance ID"
  value       = module.ec2.instance_id
}

output "app_public_ip" {
  description = "EC2 instance public IP"
  value       = module.ec2.public_ip
}

output "app_endpoint" {
  description = "Application endpoint URL"
  value       = "http://${module.ec2.public_ip}:8000"
}
