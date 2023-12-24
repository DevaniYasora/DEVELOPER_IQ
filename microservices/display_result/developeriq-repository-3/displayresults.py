from flask import Flask, jsonify
import json
from dateutil.relativedelta import relativedelta
import boto3


#Define DynamoDB tale
dynamodb_table_name = 'contributers_produtivity'

# AWS CREDENTIALS AND DETAILS
aws_access_key_id = 'your_details'
aws_secret_access_key = 'your_details'
region_name = 'ap-southeast-1'

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Get the GynamoDB table
table = dynamodb.Table(dynamodb_table_name)
# Query or scan the table to retrieve data
response = table.scan()

# Initialize Flask app
app = Flask(__name__)

# Define a route for a basic ping response
@app.route('/')
def ping():
    return "SERVICE PING SUCCESSFUL : 200"

# Function to fetch contributions productivity from dynamoDB tale
def extract_data_from_table():
    productivity_matrix_data = []

    for contributor in response['Items']:
    #extracting user_id
        user_id = contributor["user_id"]
        print("started produtivity calculation on user -",user_id)
        # Extracting ContributionsData
        productivity_data = json.loads(contributor["ContributionsData"])
        #extract data
        productivity_matrix_data.append({
            "user_id": user_id,
            "contributions": [
                {
                    "contribution_id": data["contribution_id"],
                    "login": data["login"],
                    "insert_date_time": data["insert_date_time"], # insert date time
                    "pr1_weekly": data["pr1_weekly"],
                    "pr1_monthly": data["pr1_monthly"],
                    "pr1_yearly": data["pr1_yearly"],
                    "pr2_weekly": data["pr2_weekly"],
                    "pr2_monthly": data["pr2_monthly"],
                    "pr2_yearly": data["pr2_yearly"],
                    "total_commit_stats_weekly":data["total_commit_stats_weekly"],
                    "total_commit_stats_yearly":data["total_commit_stats_yearly"],
                    "total_commit_stats_monthly":data["total_commit_stats_monthly"]
                } for data in productivity_data
            ]
        })
    return productivity_matrix_data

@app.route('/contributor/productivity_matrix')
def productivity_matrix():
    
    # Fetch contributions for the repository
    productivity_matrix_data = extract_data_from_table()

    # Return contributions as a JSON response
    if productivity_matrix_data:
        return jsonify(productivity_matrix_data)
    else:
        return jsonify({"error": "Failed to fetch contributions"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)
