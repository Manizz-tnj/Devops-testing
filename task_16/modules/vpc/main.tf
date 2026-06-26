# ----------------------------
# VPC Module
# ----------------------------
module "vpc" {
  source = "./modules/vpc"
}

# ----------------------------
# EKS Module
# ----------------------------
module "eks" {
  source = "./modules/eks"

  subnet_ids = module.vpc.public_subnet_ids
}