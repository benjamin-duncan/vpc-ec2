#!/usr/bin/env python3

from aws_cdk import core

from vpc_ec2.vpc_ec2_stack import VpcEc2Stack


app = core.App()
VpcEc2Stack(app, "vpc-ec2", env={'region': 'us-west-2'})

app.synth()
