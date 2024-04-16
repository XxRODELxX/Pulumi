"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3, ec2

# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)

sg = ec2.SecurityGroup('web-server-sg', description='Rodel web server security groups')

allow_ssh = ec2.SecurityGroupRule("AllowSSH",
                                    type="ingress",
                                    from_port=22,
                                    to_port=22,
                                    protocol="tcp", 
                                    cidr_blocks=["0.0.0.0/0"],
                                    security_group_id=sg.id
                                    )

allow_http = ec2.SecurityGroupRule("AllowHTTP",
                                    type="ingress",
                                    from_port=80,
                                    to_port=80,
                                    protocol="tcp", 
                                    cidr_blocks=["0.0.0.0/0"],
                                    security_group_id=sg.id
                                    )

allow_all_egress = ec2.SecurityGroupRule("AllowAllEgress",
                                    type="egress",
                                    from_port=0,
                                    to_port=0,
                                    protocol=-1, 
                                    cidr_blocks=["0.0.0.0/0"],
                                    security_group_id=sg.id
                                    )

instances = ["ro-web1", "ro-web2", "ro-web3"]
public_ips = []
# Create an EC2 insatce
for instance in instances:
    ec2_instance = ec2.Instance(instance,
                            ami = "ami-051f8a213df8bc089",
                            instance_type = "t2.micro",
                            vpc_security_group_ids = [sg.id],
                            key_name = "rodel",
                            tags = {
                                "Name": instance
                            }
                            )
    public_ips.append(ec2_instance.public_ip)

pulumi.export('public_ip', public_ips)
#pulumi.export('instance_url', ec2_instance.public_dns)

