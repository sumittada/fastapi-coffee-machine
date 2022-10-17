from aws_cdk import Stack
from constructs import Construct

import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_certificatemanager as acm
import aws_cdk.aws_route53 as route53
import aws_cdk.aws_ecs_patterns as ecs_patterns
import aws_cdk.aws_elasticloadbalancingv2 as elbv2


class FastAPIStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(self, "CoffeeMachineVPC", max_azs=3)

        self.ecs_cluster = ecs.Cluster(
            self,
            "CoffeeMachineECSCluster",
            vpc=self.vpc,
        )

        image = ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=ecs.ContainerImage.from_asset(
                directory="../src",
            )
        )

        hosted_zone_id = "Z05032842SUPZY34EENCQ"
        domain_name="coffee.sumit.at"

        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(self, "CoffeeHostedZone",
            hosted_zone_id=hosted_zone_id,
            zone_name="sumit.at"
        )

        self.record = route53.CnameRecord(self, "CoffeeCnameRecord",
            record_name="coffeeRecord",
            zone=hosted_zone,
            domain_name=domain_name
        )

        cert = acm.DnsValidatedCertificate(self, "CoffeeCertificate",
            domain_name=domain_name,
            hosted_zone=hosted_zone,
            region="eu-central-1"
        )

        self.ecs_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "FastAPIService",
            cluster=self.ecs_cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=1,
            task_image_options=image,
            domain_name=domain_name,
            domain_zone=hosted_zone
        )


        self.sslListener = self.ecs_service.load_balancer.add_listener("coffeeTLSListener",
            certificates=[cert],
            protocol=elbv2.ApplicationProtocol.HTTPS,
            default_target_groups=[self.ecs_service.target_group]

            )


        scalable_target = self.ecs_service.service.auto_scale_task_count(
            min_capacity=1, max_capacity=20
        )

        scalable_target.scale_on_cpu_utilization(
            "CpuScaling", target_utilization_percent=50
        )

        scalable_target.scale_on_memory_utilization(
            "MemoryScaling", target_utilization_percent=50
        )
