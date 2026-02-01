output "ec2_public_ip" {
  value = aws_instance.ai_agent.public_ip
}

output "ssh_command" {
  value = "ssh ubuntu@${aws_instance.ai_agent.public_ip}"
}