from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta
import json
import dateutil
import zulu
from dateutil.relativedelta import relativedelta
import boto3

#GITHUB token details
USER_NAME = "DevaniYasora"
token = "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"

#Define DynamoDB tale
dynamodb_table_name = 'contributers_detalis_new'

# AWS CREDENTIALS AND DETAILS
aws_access_key_id = 'AKIA5JICGBL56S3FVLQ4'
aws_secret_access_key = '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'
region_name = 'ap-southeast-1'

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Get the GynamoDB table
table = dynamodb.Table(dynamodb_table_name)

# Initialize Flask app
app = Flask(__name__)

# Define a route for a basic ping response
@app.route('/')
def ping():
    return "SERVICE PING SUCCESSFUL : 200"

# Function to fetch contributions for a GitHub repository
def fetch_repository_contributions(repo_owner, repo_name, token):

    # Delete all items in the table_produtivity
    scan_response = table.scan()
    with table.batch_writer() as batch:
        for each in scan_response['Items']:
            batch.delete_item(
                Key={
                    'user_id': each['user_id'],
                    'ContributionsData': each['ContributionsData']
                }
            )
    # GitHub API endpoint for repository contributors
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contributors"

    # Set up headers with the provided token
    headers = {
        "Authorization": f"token {token}"
    }

    # Make the API request
    response = requests.get(url, headers=headers)
        
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        contributions = response.json()
        
        # Extracting contributor information
        i=0
        contributor_info_final = []
        for contributor in contributions:
            i=i+1
            contributor_info = []
            contributor_id = contributor['id']
            login = contributor['login']
            num_commits = contributor['contributions']
            weekly_stats = get_commit_stats(repo_owner, repo_name, login, token, 'week')
            monthly_stats = get_commit_stats(repo_owner, repo_name, login, token, 'month')
            yearly_stats = get_commit_stats(repo_owner, repo_name, login, token, 'year')
            weekly_comment, monthly_comments, yearly_comments,issues_created_weekly,issues_created_monthly,issues_created_yearly = CONTRIBUTOR_ISSUES_URI__(repo_owner, repo_name, login, token)
            contributor_info.append({
                "insert_date_time" : str(datetime.now()),
                "ID": contributor_id,
                "LOGIN": login,
                "TOTAL_COMMITS": num_commits,
                "WEEKLY_STATUS": {
                    "commit_stats_weekly": weekly_stats,
                    "comments_weekly": weekly_comment,
                    "issues_created_weekly": issues_created_weekly
                },
                "MONTHLY_STATUS": {
                    "commit_stats_monthly": monthly_stats,
                    "comments_monthly": monthly_comments,
                    "issues_created_monthly": issues_created_monthly
                },
                "YEARLY_STATUS": {
                    "commit_stats_yearly": yearly_stats,
                    "comments_yearly": yearly_comments,
                    "issues_created_yearly": issues_created_yearly
                }            
            })

            # Write to DynamoDB
            contributor_info=json.dumps(contributor_info)
            table.put_item(
                Item={
                    'user_id': str(contributor_id),
                    'ContributionsData': contributor_info
                }
            )
            contributor_info_final.append(contributor_info)

        return contributions, contributor_info_final
        
    elif response.status_code == 202:
        print(f"Contributions computation in progress. Retrying in 10 seconds...")

    return None, None

# Function to get commit statistics for a contributor within a specified time frame
def get_commit_stats(repo_owner, repo_name, contributor_login, token, time_frame):
    # Get the current date
    print("get_commit_stats function started for:",contributor_login)
    current_date = datetime.now()

    # Calculate the start date based on the time frame
    if time_frame == 'week':
        start_date = str(zulu.parse(datetime.now() - dateutil.relativedelta.relativedelta(weeks=1))).split('.')[0]
        print("WEEK:",start_date)
        start_date_new = zulu.parse(datetime.now() - relativedelta(weeks=1)).timestamp()
    elif time_frame == 'month':
        start_date=str(zulu.parse(datetime.now() - dateutil.relativedelta.relativedelta(months=1))).split('.')[0]
        start_date_new = zulu.parse(datetime.now() - relativedelta(months=1)).timestamp()
        print("MONTH:",start_date)
    elif time_frame == 'year':
        start_date = str(zulu.parse(datetime.now() - dateutil.relativedelta.relativedelta(years=1))).split('.')[0]
        start_date_new = zulu.parse(datetime.now() - relativedelta(years=1)).timestamp()
        print("YEAR:",start_date)
    else:
        start_date = current_date


# Convert to int
    start_date_new= int(start_date_new)

    # Fetch commit stats for the specified time frame
    stats_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/stats/contributors"
    stats_url_request  = f"{stats_url}?creator={contributor_login}&since={start_date}"
    response = requests.request("GET",stats_url_request,auth=(USER_NAME,token))

    if response.status_code == 200:
        stats = response.json()
        
        # Find the contributor in the stats
        for contributor_stats in stats:
            if contributor_stats["author"]["login"] == contributor_login:
                # Extract the weeks data
                weeks_data = contributor_stats.get("weeks", [])
                #print("weeks_data:",weeks_data)
                # Filter the weeks based on the start date
                
                total_additions = 0
                total_deletions = 0
                total_commits   = 0

                for week in weeks_data:
                    week_timestamp = week.get("w", 0)
                    week_date = week_timestamp

                    if start_date_new <= week_date:
                        total_additions += week.get("a", 0)
                        total_deletions += week.get("d", 0)
                        total_commits += week.get("c", 0)
                        

                # If any relevant weeks are found, append them to the statistics
                statistics=[]
                statistics.append({
                    "a":total_additions,
                    "d":total_deletions,
                    "c":total_commits})
                    
        return statistics

# Function to retrieve contributor issues and comments
def CONTRIBUTOR_ISSUES_URI__(repo_owner, repo_name, contributor_login, token):
    print("CONTRIBUTOR_ISSUES_URI__ function started for:",contributor_login)

    contributor_issue_comments_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/comments"
    contributor_issues_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"

    year_since  = str(zulu.parse(datetime.now() - dateutil.relativedelta.relativedelta(years=1))).split('.')[0]
    week_since  = str(zulu.parse(datetime.now() - dateutil.relativedelta.relativedelta(weeks=1))).split('.')[0]
    month_since = str(zulu.parse(datetime.now() - dateutil.relativedelta.relativedelta(months=1))).split('.')[0]

    contributor_issue_stats_url_year  = f"{contributor_issues_url}?creator={contributor_login}&since={year_since}"
    contributor_issue_stats_url_week  = f"{contributor_issues_url}?creator={contributor_login}&since={week_since}"
    contributor_issue_stats_url_month = f"{contributor_issues_url}?creator={contributor_login}&since={month_since}"

    num_issues_created_year  = len(requests.request("GET",contributor_issue_stats_url_year,auth=(USER_NAME,token)).json())
    num_issues_created_week  = len(requests.request("GET",contributor_issue_stats_url_week,auth=(USER_NAME,token)).json())
    num_issues_created_month = len(requests.request("GET",contributor_issue_stats_url_month,auth=(USER_NAME,token)).json())

    contributor_comments_url_year = f"{contributor_issue_comments_url}?since={year_since}"
    contributor_comments_url_month = f"{contributor_issue_comments_url}?since={month_since}"
    contributor_comments_url_week = f"{contributor_issue_comments_url}?since={week_since}"

    num_comments_year = len([comment for comment in requests.request("GET",contributor_comments_url_year,auth=(USER_NAME,token)).json() if comment["user"]["login"]==contributor_login])
    num_comments_month = len([comment for comment in requests.request("GET",contributor_comments_url_month,auth=(USER_NAME,token)).json() if comment["user"]["login"]==contributor_login])
    num_comments_week = len([comment for comment in requests.request("GET",contributor_comments_url_week,auth=(USER_NAME,token)).json() if comment["user"]["login"]==contributor_login])

    return num_comments_week,num_comments_month,num_comments_year,num_issues_created_month,num_issues_created_week,num_issues_created_year

@app.route('/contributor/get_contributions')
def get_contributions():
    # Replace these values with the actual repository owner, name, and token
    repo_owner = "freeCodeCamp"
    repo_name = "mobile"
    github_token = "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"

    # Fetch contributions for the repository
    contributions, contributor_info = fetch_repository_contributions(repo_owner, repo_name, github_token)

    # Save contributor_info to a JSON file
    json_filename = 'contributor_info.json'
    with open(json_filename, 'w') as json_file:
        json.dump(contributor_info, json_file, indent=2)

    # Return contributions as a JSON response
    if contributions:
        return contributor_info
    else:
        return jsonify({"error": "Failed to fetch contributions"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
