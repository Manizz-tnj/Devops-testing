import boto3

table_name = "customer-data"

ddb = boto3.resource("dynamodb", region_name="ap-south-1")
table = ddb.Table(table_name)

table.put_item(
    Item={
        "id":"1",
        "name":"Mani"
    }
)

print("PutItem Success")

response = table.get_item(
    Key={"id":"1"}
)

print(response)

table.update_item(
    Key={"id":"1"},
    UpdateExpression="SET #n=:v",
    ExpressionAttributeNames={
        "#n":"name"
    },
    ExpressionAttributeValues={
        ":v":"Manish"
    }
)

print("UpdateItem Success")