import json

from aws_cdk import (
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_secretsmanager as secretsmanager,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticloadbalancingv2 as elbv2,
    core
)

class VpcEc2Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self,
            "VPC",
            max_azs=2,
            # cidr="10.30.0.0/16",
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="Public1",
                    cidr_mask=24
                )]
                # ec2.SubnetConfiguration(
                #     subnet_type=ec2.SubnetType.PUBLIC,
                #     name="Public2",
                #     cidr_mask=24
                # ),

            #     ec2.SubnetConfiguration(
            #         subnet_type=ec2.SubnetType.ISOLATED,
            #         name="Isolated1a",
            #         cidr_mask=24,
            #     ),
            # ]
        )

        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        cluster.add_capacity("ASG", instance_type = ec2.InstanceType("t2.micro"),key_name="NewKP")

        cluster_sg = ec2.SecurityGroup(
            self,
            "ClusterSG",
            vpc=vpc,
            allow_all_outbound=True
        )

        cluster_sg.add_ingress_rule(ec2.Peer.any_ipv4(),ec2.Port.tcp(22),"SSH")
        cluster.connections.add_security_group(cluster_sg)

        task = ecs.Ec2TaskDefinition(self,"TaskDefinition",) # network_mode="awsvpc")

        container = task.add_container(
            "App",
            image=ecs.ContainerImage.from_asset("./app"),
            memory_limit_mib=256,
            environment={
                "HELLO_WORLD": "Hello, world!"
            }
        )

        port_mapping = ecs.PortMapping(
            container_port = 8000,
            host_port = 0,
            protocol=ecs.Protocol.TCP
        )

        container.add_port_mappings(port_mapping)

        service = ecs.Ec2Service(
            self,
            "Service",
            task_definition=task,
            # assign_public_ip=True,
            cluster=cluster,

        )

        alb = elbv2.ApplicationLoadBalancer(self, "LB",vpc=vpc,internet_facing=True)

        listener = alb.add_listener("Listener",port=80,open=True)

        health_check = elbv2.HealthCheck(
            interval = core.Duration.seconds(60),
            path="/health/",
            timeout = core.Duration.seconds(5)
        )

        listener.add_targets(
            "ECS",
            port=80,
            targets=[service],
            health_check=health_check
        )
"""
        role = iam.Role(
            self,
            "InstanceSSM",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )

        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )


        ecs_linux2 = ecs.MachineImageType.AMAZON_LINUX_2
        security_group = ec2.SecurityGroup(
            self,
            "SecurityGroup",
            vpc=vpc,
            allow_all_outbound=True
        )

        security_group.add_ingress_rule(ec2.Peer.any_ipv4(),ec2.Port.tcp(22),"SSH")

        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "yum install -y aws-cli",

        )
        instance = ec2.Instance(
            self,
            "Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=amzn_linux,
            vpc=vpc,
            role=role,
            key_name="NewKP",
            security_group=security_group,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            user_data=user_data,
        )

        db_secret = secretsmanager.Secret(
            self,
            "DBSecret",
            secret_name="db-secret",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template=json.dumps({"username": "postgres"}),
                exclude_punctuation=True,
                include_space=False,
                generate_string_key="password"
            )
        )

        database = rds.DatabaseInstance(
            self,
            "Database",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_12_4),
            instance_type=ec2.InstanceType("t2.micro"),
            vpc = vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.ISOLATED),
            credentials=rds.Credentials.from_secret(db_secret)
            


        )
"""

"""         
        task = ecs.FargateTaskDefinition(self, "TaskDefinition")

        task.add_container(
            "App",
            image=ecs.ContainerImage.from_asset("./app"),
            memory_limit_mib=512,
            environment={
                "HELLO_WORLD": "Hello, world!"
            }
        ).add_port_mappings(ecs.PortMapping(container_port=8000, host_port=8000))


        app_service = ecs_patterns.NetworkLoadBalancedFargateService(
            self,
            "Service",
            service_name="django-service",
            cluster=cluster,
            cpu=256,  # Default is 256
            desired_count=1,  # Default is 1
            task_definition=task,
            memory_limit_mib=512,  # Default is 512
            listener_port=80,
            public_load_balancer=True,
            assign_public_ip=True
        )

        app_service.service.connections.allow_from_any_ipv4(
            ec2.Port.tcp(8000),"django"
        )
"""