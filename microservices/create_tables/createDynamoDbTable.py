import boto3

# Your AWS credentials and region
aws_access_key_id = 'your_details'
aws_secret_access_key = 'your_details'
region_name = 'ap-southeast-1'

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Define the table name
table_name = 'contributers_produtivity'

# Create the table
table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
        {
            'AttributeName': 'user_id',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': "ContributionsData",
            'KeyType': "RANGE"
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'user_id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'ContributionsData',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 3,
        'WriteCapacityUnits': 3
    }
)

# Wait for the table to be created
table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

# Print the details of the created table
print("Table status:", table.table_status)
