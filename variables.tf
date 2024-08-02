variable "project" {
  default = "MovieRating-Analysis"
}

variable "environment" {
  default = "Development"
}

variable "name" {
  default = "gfk"
}

variable "vpc_id" {
  default = "vpc-0d56cf1543ad20663"
}

variable "release_label" {
  default = "emr-7.2.0"
}

variable "applications" {
  default = ["Hadoop", "Hive", "Spark", "JupyterEnterpriseGateway", "Livy"]
}

variable "key_name" {
  default = "ec2-gfk"  # Ensure this key pair exists in specified region
}

variable "subnet_id" {
  default = "subnet-01ee0eaed701280dd"
}

variable "bootstrap_name" {
  default = "test_bootstrap"
}

variable "bootstrap_uri" {
  default = "s3://movielens-gfk/bootstrap/bootstrap.sh"
}

variable "bootstrap_args" {
  default = ["instance.isMaster=true", "echo running on master node"]
}
