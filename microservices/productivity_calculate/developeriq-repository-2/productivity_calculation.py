import boto3
import json
import math
from datetime import datetime
from flask import Flask, jsonify

# AWS CREDENTIALS AND DETAILS
aws_access_key_id = 'your_details'
aws_secret_access_key = 'your_details'
region_name = 'ap-southeast-1'

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Define DynamoDB table name
dynamodb_table_name = 'contributers_detalis_new'
dynamodb_productivity_table_name = 'contributers_produtivity'

# Get the DynamoDB table
table = dynamodb.Table(dynamodb_table_name)
table_produtivity = dynamodb.Table(dynamodb_productivity_table_name)

# Initialize Flask app
app = Flask(__name__)

# Define a route for a basic ping response
@app.route('/')
def ping():
    return "SERVICE PING SUCCESSFUL : 200"

@app.route('/contributor/cal_produtivity')
def get_contributions():
    
    # Delete all items in the table_produtivity
    scan_response = table_produtivity.scan()
    with table_produtivity.batch_writer() as batch:
        for each in scan_response['Items']:
            batch.delete_item(
                Key={
                    'user_id': each['user_id'],
                    'ContributionsData': each['ContributionsData']
                }
            )

    # Query or scan the table to retrieve data
    response = table.scan()
    productivity_data_final = []
    # Print the retrieved items
    for contributor in response['Items']:
        #extracting user_id
        login = contributor['user_id']
        print("started produtivity calculation on user -",login)
        # Extracting ContributionsData
        contributions_data = contributor['ContributionsData']
        
        # Converting ContributionsData from string to a list of dictionaries
        contributions_list = json.loads(contributions_data)

        for contribution in contributions_list:
            # Dictionary to store productivity for each contributor
            productivity_data = []

            #extract data
            insert_date_time = contribution['insert_date_time']
            contribution_id = contribution['ID']
            login = contribution['LOGIN']
            total_commits = contribution['TOTAL_COMMITS']

            # Extracting weekly status
            weekly_status = contribution['WEEKLY_STATUS']
            commit_stats_weekly = weekly_status['commit_stats_weekly']
            comments_weekly = weekly_status['comments_weekly']
            issues_created_weekly = weekly_status['issues_created_weekly']
            
            # Extracting 'a', 'd', and 'c' values
            if commit_stats_weekly:
                a_value_weekly = float(commit_stats_weekly[0]['a'])
                d_value_weekly = float(commit_stats_weekly[0]['d'])
                c_value_weekly = float(commit_stats_weekly[0]['c'])
            else:
                 a_value_weekly = 0
                 d_value_weekly = 0
                 c_value_weekly = 0

            # Extracting monthly status
            monthly_status = contribution['MONTHLY_STATUS']
            commit_stats_monthly = monthly_status['commit_stats_monthly']
            comments_monthly = monthly_status['comments_monthly']
            issues_created_monthly = monthly_status['issues_created_monthly']

            # Extracting 'a', 'd', and 'c' values
            if commit_stats_monthly:
                a_value_monthly = float(commit_stats_monthly[0]['a'])
                d_value_monthly = float(commit_stats_monthly[0]['d'])
                c_value_monthly = float(commit_stats_monthly[0]['c'])
            else:
                 a_value_monthly = 0
                 d_value_monthly = 0
                 c_value_monthly = 0

            # Extracting yearly status
            yearly_status = contribution['YEARLY_STATUS']
            commit_stats_yearly = yearly_status['commit_stats_yearly']
            comments_yearly = yearly_status['comments_yearly']
            issues_created_yearly = yearly_status['issues_created_yearly']

            # Extracting 'a', 'd', and 'c' values
            if commit_stats_yearly:
                a_value_yearly = float(commit_stats_yearly[0]['a'])
                d_value_yearly = float(commit_stats_yearly[0]['d'])
                c_value_yearly = float(commit_stats_yearly[0]['c'])
            else:
                 a_value_yearly = 0
                 d_value_yearly = 0
                 c_value_yearly = 0

            #productivity matrix 1
            pr1_weekly = float(comments_weekly) + float(issues_created_weekly)
            pr1_monthly = float(comments_monthly) + float(issues_created_monthly)
            pr1_yearly = float(comments_yearly) + float(issues_created_yearly)

            #productivity Matrix 2 # commit productivity
            # Avoid division by zero
            if c_value_weekly != 0:
                pr2_weekly = math.log10((a_value_weekly + d_value_weekly) / c_value_weekly)
            else: 
                pr2_weekly = 0
            
            if c_value_monthly != 0:
                pr2_monthly = math.log10((a_value_monthly + d_value_monthly) / c_value_monthly)
            else:
                pr2_monthly = 0

            if c_value_yearly != 0:
                pr2_yearly = math.log10((a_value_yearly + d_value_yearly) / c_value_yearly)
            else: 
                pr2_yearly = 0
            

            # Store monthly productivity in the dictionary
            productivity_data.append({"contribution_id":contribution_id,
                                    "login":login,
                                    "insert_date_time":str(datetime.now()),
                                "total_commit_stats_weekly":commit_stats_weekly,
                                "total_commit_stats_yearly":commit_stats_yearly,
                                "total_commit_stats_monthly":commit_stats_monthly,
                                "pr1_weekly":pr1_weekly,
                                "pr1_monthly":pr1_monthly,
                                "pr1_yearly":pr1_yearly,
                                "pr2_weekly":pr2_weekly,
                                "pr2_monthly":pr2_monthly,
                                "pr2_yearly":pr2_yearly})
            
            # Write to DynamoDB
            productivity_data=json.dumps(productivity_data)
            print(productivity_data)
            table_produtivity.put_item(
                    Item={
                        'user_id': str(contribution_id),
                        'ContributionsData': productivity_data
                    }
                )
        productivity_data_final.append(productivity_data)
    return jsonify({"message": "Productivity calculation completed."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)

