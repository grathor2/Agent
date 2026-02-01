data "aws_ami" "ubuntu_arm" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-arm64-server-*"]
  }

  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

resource "aws_instance" "ai_agent" {
  ami                    = data.aws_ami.ubuntu_arm.id
  instance_type          = "t4g.medium"
  subnet_id = data.aws_subnets.default.ids[0]
  vpc_security_group_ids = [aws_security_group.ai_agent_sg.id]
  key_name               = aws_key_pair.deep_matrix.key_name

  associate_public_ip_address = true

  root_block_device {
    volume_type = "gp3"
    volume_size = 20
  }

user_data = file("${path.module}/user_data.sh")

  tags = {
    Team = "Deep-Matrix"
    Name = "Deep-Matrix"
  }
}