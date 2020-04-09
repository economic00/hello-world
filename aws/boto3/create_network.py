import boto3
import time

client = boto3.client('ec2')

vpc_new = client.create_vpc(CidrBlock='10.0.0.0/16', InstanceTenancy='default')

vpc_info = vpc_new['Vpc']
vpc_id = vpc_info['VpcId']

time.sleep(2)

tag = client.create_tags(Resources = [vpc_id], Tags = [{'Key': 'Name', 'Value': 'TestVpc00'}])
print(vpc_id)

#create IG and attach to VPC
internet_gateway = client.create_internet_gateway()

internet_gateway_info = internet_gateway['InternetGateway']
internet_gateway_id = internet_gateway_info['InternetGatewayId']

attach_gateway = client.attach_internet_gateway(InternetGatewayId = internet_gateway_id, VpcId = vpc_id)

#create subnet
subnet_response = client.create_subnet(
    CidrBlock='10.0.1.0/24',
    VpcId = vpc_id
)

subnet_info = subnet_response['Subnet']
subnet_id = subnet_info['SubnetId']
vpc_of_subnet = subnet_info['VpcId']

print(subnet_id, vpc_of_subnet)

#describe routing

routes = client.describe_route_tables(
    Filters = [{'Name': 'vpc-id','Values': [vpc_id]}])

route_info = routes['RouteTables']

for route in route_info:
    route_associations = route['Associations']

    for route_inner_info in route_associations:
        route_id = route_inner_info['RouteTableId']
        print (route_id)

#create a route to the internet
new_route = client.create_route(DestinationCidrBlock = '0.0.0.0/0', GatewayId = internet_gateway_id, RouteTableId = route_id)

print(new_route)
