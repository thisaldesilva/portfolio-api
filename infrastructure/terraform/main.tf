# Main Terraform configuration for AWS infrastructure.

terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # S3 backend disabled for initial setup - state will be stored locally
  # To enable remote state storage, uncomment and configure:
  # backend "s3" {
  #   bucket = "your-terraform-state-bucket"
  #   key    = "portfolio-api/terraform.tfstate"
  #   region = "us-east-1"
  #   dynamodb_table = "terraform-state-lock"
  #   encrypt = true
  # }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "Portfolio Management API"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

# VPC
module "vpc" {
  source = "./modules/vpc"

  environment         = var.environment
  vpc_cidr            = var.vpc_cidr
  availability_zones  = data.aws_availability_zones.available.names
  public_subnet_cidrs = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
}

# Security Groups
module "security_groups" {
  source = "./modules/security"

  environment = var.environment
  vpc_id      = module.vpc.vpc_id
  allowed_ssh_cidr = var.allowed_ssh_cidr
}

# RDS Database
module "rds" {
  source = "./modules/rds"

  environment           = var.environment
  vpc_id                = module.vpc.vpc_id
  private_subnet_ids    = module.vpc.private_subnet_ids
  db_security_group_id  = module.security_groups.db_security_group_id
  db_instance_class     = var.db_instance_class
  db_name               = var.db_name
  db_username           = var.db_username
  db_password           = var.db_password
  allocated_storage     = var.db_allocated_storage
}

# EC2 Application Server
module "ec2" {
  source = "./modules/ec2"

  environment             = var.environment
  vpc_id                  = module.vpc.vpc_id
  public_subnet_ids       = module.vpc.public_subnet_ids
  app_security_group_id   = module.security_groups.app_security_group_id
  instance_type           = var.instance_type
  key_name                = var.key_name
  db_endpoint             = module.rds.db_endpoint
  db_name                 = var.db_name
  db_username             = var.db_username
  db_password             = var.db_password
}
