# RDS Module

# DB Subnet Group
resource "aws_db_subnet_group" "main" {
  name       = "${var.environment}-portfolio-db-subnet-group"
  subnet_ids = var.private_subnet_ids

  tags = {
    Name = "${var.environment}-db-subnet-group"
  }
}

# RDS PostgreSQL Instance
resource "aws_db_instance" "main" {
  identifier     = "${var.environment}-portfolio-db"
  engine         = "postgres"
  engine_version = "16.3"

  instance_class    = var.db_instance_class
  allocated_storage = var.allocated_storage
  storage_type      = "gp3"
  storage_encrypted = true

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [var.db_security_group_id]

  # Backup configuration
  backup_retention_period = 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "mon:04:00-mon:05:00"

  # High availability - Disabled for free tier compatibility
  multi_az               = false
  publicly_accessible    = false
  skip_final_snapshot    = true
  final_snapshot_identifier = null

  # Performance Insights - Disabled for free tier
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  performance_insights_enabled    = false
  performance_insights_retention_period = 0

  # Auto minor version upgrade
  auto_minor_version_upgrade = true

  tags = {
    Name = "${var.environment}-portfolio-db"
  }
}
