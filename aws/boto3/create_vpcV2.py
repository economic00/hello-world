import boto3

client = boto3.client('ec2')

vpc = client.create_vpc(CidrBlock='10.0.0.0/16', InstanceTenancy='default')

#tag_vpc = client.create_tags(Tags=[{"Key": "Name", "Value": "testVpc00"}])
#vpc.wait_until_available()

vpc_info = client.describe_vpcs()
vpcs = vpc_info['Vpcs']

#print(vpcs)

for vpc in vpcs:
    #print(vpc)
    is_default = vpc['IsDefault']
    cidr_block = vpc['CidrBlock']
    vpc_id = vpc['VpcId']
    #print(is_default)
    if is_default == False and cidr_block == '10.0.0.0/16':
        #print('Tag this one')
        #print(vpc_id)
        tag = client.create_tags(Resources = [vpc_id], Tags = [{'Key': 'Name', 'Value': 'TestVpc00'}])
        #print(tag)
    #else:
    #    print("Hello World")

#create IG
internet_gateway = client.create_internet_gateway()

#describe the gateway
desc_gateway = client.describe_internet_gateways()
gateways = desc_gateway['InternetGateways']

for gateway in gateways:
    #print(gateway)
    gateway_id = gateway['InternetGatewayId']
    attachments = gateway['Attachments']
    #print(attachments)
    if len(attachments) == 0:
        print(gateway_id)
        #print(vpc_id)
        attach_gateway = client.attach_internet_gateway(
        InternetGatewayId = gateway_id,
        VpcId = vpc_id)

     
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

route_info = routes['Associations']
route_id = route_info['RouteTableId']

#print(route_info)


print(route_id)

#response = client.create_route(RouteTableId=route_id)