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
        print(tag)
    #else:
    #    print("Hello World")


#create IG
c_internet_gateway = client.create_internet_gateway()

#describe the gateway
desc_gateway = client.describe_internet_gateways()
gateway = desc_gateway['InternetGateways']

#if gateway is unattached
print(gateway)


#attach gateway to vpc
a_internet_gateway = client.attach_internet_gateway(
    InternetGatewayId='string',
    VpcId='string'
)

#create subnet

#assign routing



