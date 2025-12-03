terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "cv_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "CV App VPC"
  }
}

resource "aws_subnet" "cv_subnet" {
  vpc_id     = aws_vpc.cv_vpc.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = "CV App Subnet"
  }
}

resource "aws_security_group" "cv_sg" {
  name_prefix = "cv-app-sg"
  vpc_id      = aws_vpc.cv_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "CV App Security Group"
  }
}

resource "aws_instance" "cv_app" {
  ami           = "ami-0c55b159cbfafe1d0"  # Ubuntu 20.04 LTS
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.cv_subnet.id
  vpc_security_group_ids = [aws_security_group.cv_sg.id]

  tags = {
    Name = "CV App Server"
  }

  user_data = <<-EOF
              #!/bin/bash
              sudo apt update
              sudo apt install -y docker.io docker-compose
              sudo systemctl start docker
              sudo systemctl enable docker
              EOF
}

resource "aws_ssm_parameter" "db_username" {
  name  = "/cv-app/db/username"
  type  = "String"
  value = "cv_user"
}

resource "aws_ssm_parameter" "db_password" {
  name  = "/cv-app/db/password"
  type  = "SecureString"
  value = "cv_password"
}

resource "aws_db_instance" "cv_db" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "13"
  instance_class       = "db.t3.micro"
  db_name              = "cv_db"
  username             = aws_ssm_parameter.db_username.value
  password             = aws_ssm_parameter.db_password.value
  parameter_group_name = "default.postgres13"
  skip_final_snapshot  = true
  vpc_security_group_ids = [aws_security_group.cv_sg.id]
  db_subnet_group_name = aws_db_subnet_group.cv_db_subnet.name

  tags = {
    Name = "CV Database"
  }
}

resource "aws_db_subnet_group" "cv_db_subnet" {
  name       = "cv-db-subnet-group"
  subnet_ids = [aws_subnet.cv_subnet.id]

  tags = {
    Name = "CV DB Subnet Group"
  }
}

output "instance_ip" {
  value = aws_instance.cv_app.public_ip
}

output "db_endpoint" {
  value = aws_db_instance.cv_db.endpoint
}
