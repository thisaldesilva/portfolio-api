# EC2 Module

# Get latest Amazon Linux 2023 AMI (ARM64 for t4g instances)
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-arm64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# IAM Role for EC2
resource "aws_iam_role" "app" {
  name = "${var.environment}-portfolio-app-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "${var.environment}-app-role"
  }
}

# Attach policies to IAM role
resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.app.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role_policy_attachment" "cloudwatch" {
  role       = aws_iam_role.app.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

# IAM Instance Profile
resource "aws_iam_instance_profile" "app" {
  name = "${var.environment}-portfolio-app-profile"
  role = aws_iam_role.app.name
}

# User data script
locals {
  user_data = <<-EOF
    #!/bin/bash
    set -e

    # Update system
    yum update -y

    # Install Python 3.11
    yum install -y python3.11 python3.11-pip git

    # Install PostgreSQL client
    yum install -y postgresql15

    # Create application directory
    mkdir -p /opt/portfolio-api
    chown ec2-user:ec2-user /opt/portfolio-api

    # Create systemd service file
    cat > /etc/systemd/system/portfolio-api.service <<'SERVICE'
    [Unit]
    Description=Portfolio Management API
    After=network.target

    [Service]
    Type=simple
    User=ec2-user
    WorkingDirectory=/opt/portfolio-api
    Environment="PATH=/usr/local/bin:/usr/bin:/bin"
    EnvironmentFile=/opt/portfolio-api/.env
    ExecStart=/usr/local/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
    Restart=always
    RestartSec=10

    [Install]
    WantedBy=multi-user.target
    SERVICE

    # Enable the service
    systemctl daemon-reload
    systemctl enable portfolio-api

    echo "EC2 instance setup complete"
  EOF
}

# EC2 Instance
resource "aws_instance" "app" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  key_name               = var.key_name
  subnet_id              = var.public_subnet_ids[0]
  vpc_security_group_ids = [var.app_security_group_id]
  iam_instance_profile   = aws_iam_instance_profile.app.name

  user_data = local.user_data

  root_block_device {
    volume_size           = 30
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  tags = {
    Name = "${var.environment}-portfolio-app"
  }
}

# Elastic IP for EC2
resource "aws_eip" "app" {
  instance = aws_instance.app.id
  domain   = "vpc"

  tags = {
    Name = "${var.environment}-app-eip"
  }
}
