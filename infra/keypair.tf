resource "aws_key_pair" "deep_matrix" {
  key_name   = "deep-matrix"
  public_key = file("~/.ssh/deep-matrix.pub")

  tags = {
    Team = "Deep-Matrix"
  }
}