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

resource "aws_instance" "cv_app" {
  ami           = "ami-0c55b159cbfafe1d0"  # Ubuntu 20.04 LTS
  instance_type = "t2.micro"

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

resource "aws_db_instance" "cv_db" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "13"
  instance_class       = "db.t3.micro"
  db_name              = "cv_db"
  username             = "cv_user"
  password             = "cv_password"
  parameter_group_name = "default.postgres13"
  skip_final_snapshot  = true

  tags = {
    Name = "CV Database"
  }
}

output "instance_ip" {
  value = aws_instance.cv_app.public_ip
}

output "db_endpoint" {
  value = aws_db_instance.cv_db.endpoint
}
