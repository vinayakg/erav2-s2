### Step 1: Create IAM User

Login to AWS Console with your root account
Go to IAM Service → Users → Create User

User Configuration:

User name: animal-app-developer (or your preferred name)
AWS access type: ✅ Programmatic access (for CLI/SDK)
Console access: ❌ No (more secure, you have root for console)

### Step 2: Create Custom Policy
Instead of using AWS managed policies (which are too broad), let's create a minimal policy:
Policy Name: AnimalAppDeveloperPolicy
JSON Policy (I'll provide this next):

`
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EC2Management",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:DescribeImages",
                "ec2:DescribeKeyPairs",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeVpcs",
                "ec2:DescribeSubnets",
                "ec2:DescribeAddresses",
                "ec2:RunInstances",
                "ec2:StartInstances",
                "ec2:StopInstances",
                "ec2:RebootInstances",
                "ec2:TerminateInstances",
                "ec2:CreateKeyPair",
                "ec2:DeleteKeyPair",
                "ec2:ImportKeyPair",
                "ec2:CreateSecurityGroup",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:RevokeSecurityGroupIngress",
                "ec2:RevokeSecurityGroupEgress",
                "ec2:DeleteSecurityGroup",
                "ec2:AllocateAddress",
                "ec2:AssociateAddress",
                "ec2:DisassociateAddress",
                "ec2:ReleaseAddress",
                "ec2:CreateTags",
                "ec2:DescribeTags"
            ],
            "Resource": "*"
        },
        {
            "Sid": "RDSManagement",
            "Effect": "Allow",
            "Action": [
                "rds:DescribeDBInstances",
                "rds:DescribeDBSubnetGroups",
                "rds:DescribeDBParameterGroups",
                "rds:DescribeDBSecurityGroups",
                "rds:CreateDBInstance",
                "rds:DeleteDBInstance",
                "rds:ModifyDBInstance",
                "rds:StartDBInstance",
                "rds:StopDBInstance",
                "rds:CreateDBSubnetGroup",
                "rds:DeleteDBSubnetGroup",
                "rds:AddTagsToResource",
                "rds:ListTagsForResource"
            ],
            "Resource": "*"
        },
        {
            "Sid": "S3Management",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:CreateBucket",
                "s3:DeleteBucket",
                "s3:GetBucketLocation",
                "s3:ListAllMyBuckets"
            ],
            "Resource": [
                "arn:aws:s3:::animal-app-*",
                "arn:aws:s3:::animal-app-*/*"
            ]
        }
    ]
}
`

Once you confirm, I'll walk you through:

Creating the policy in AWS console
Attaching it to the user
Generating access keys
Testing AWS CLI configuration

`
aws sts get-caller-identity  # Test your current AWS CLI setup
`

## Step-by-Step AWS CLI Commands:
### Step 1: Create Security Group

# Create security group
`aws ec2 create-security-group \
    --group-name vgerav4-s2-sg \
    --description "Security group for animal app server" \
    --region us-east-1`    

### Step 2: Add Security Group Rules


# SSH access from your IP only
`aws ec2 authorize-security-group-ingress \
    --group-name vgerav4-s2-sg \
    --protocol tcp \
    --port 22 \
    --cidr 11.22.33.44/32 \
    --region us-east-1`

# HTTP access from anywhere
`aws ec2 authorize-security-group-ingress \
    --group-name vgerav4-s2-sg \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0 \
    --region us-east-1`

# HTTPS access from anywhere  
`aws ec2 authorize-security-group-ingress \
    --group-name vgerav4-s2-sg \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0 \
    --region us-east-1`

# FastAPI access from anywhere
`aws ec2 authorize-security-group-ingress \
    --group-name vgerav4-s2-sg \
    --protocol tcp \
    --port 8000 \
    --cidr 0.0.0.0/0 \
    --region us-east-1`
### Step 3: Find Ubuntu 22.04 AMI ID

`aws ec2 describe-images \
    --owners 099720109477 \
    --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" \
    --query 'Images | sort_by(@, &CreationDate) | [-1].ImageId' \
    --output text \
    --region us-east-1`

### Step 4: Launch EC2 Instance
`
# Launch EC2 instance (replace AMI_ID with the output from above)
`aws ec2 run-instances \
    --image-id AMI_ID \
    --count 1 \
    --instance-type t3a.micro \
    --key-name ab-yho \
    --security-groups vgerav4-s2-sg \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=erav4-s2}]' \
    --region us-east-1`

### Step 5: Import Key pair

`aws ec2 import-key-pair \
    --key-name ab-yho \
    --public-key-material fileb://~/.ssh/id_rsa.pub \
    --region us-east-1`


