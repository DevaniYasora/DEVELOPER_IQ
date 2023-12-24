# DEVELOPER_IQ
Productivity calculation solution 

This productivity calculation solution has been developed for the CMM707-Cloud Computing module, conducted as part of the master's degree program at Robert Gordon University in the UK.

**Case Study**
The IT department of AcmeCorp has contacted you to develop a solution known as DeveloperIQ.
DeveloperIQ is a developer productivity tracker. Its main purpose is to track how productive a developer is. You are required to design a microservice architecture which would run on a
Kubernetes cluster. Your solution needs to consider the following attributes;
● Scalable
● Secure
● Fault tolerant
● Affordable.
You need to identify at least three metrics that can be extracted by integrating with the Github REST API (https://docs.github.com/en/rest/reference) (eg:- Commits of searched user,
Issues for user could be example metrics, students are allowed to come up with relevant metrics)

Store your metrics in either an RDS or AWS DynamoDB database outside of the Kubernetes cluster.
Observability infrastructure is deployed on the same Kubernetes cluster and all the solutions deployed into the Kubernetes cluster are observed using this solution.
Also, the IT department wants to automate the service build and deployment of this solution using a CI/CD pipeline. They want to maintain the 100% uptime of all the services by using the rolling-out deployment strategy. Using an integration test suite, they want to test their solution automatically after every deployment. Also, they want to test the solution periodically with the same test suite.

**
Solution:**
> **Deploying a Python-based Microservice Application on AWS EKS**

**DEVELOPERIQ SOLUTION**
Repository Details
  Repo Owner :freeCodeCamp | Repo Name : Mobile
  
productivity matrix: 1 : Summarized collected data
  Calculated each and every developer’s total commit addition, total commit deletions, total number of commits in weekly, monthly and yearly basis
Summarize the number of issues created and issues comments for each developer for a weekly, monthly and yearly basis.

productivity matrix: 2 : User's productivity based on their interactions
Matrix 1 is calculated by combining the counts of comments and issues created by a developer. Reflects a user's productivity based on their interactions, such as comments and issues created, over different time intervals (weekly, monthly, and yearly). 
![image](https://github.com/DevaniYasora/DEVELOPER_IQ/assets/64655854/6f82608c-c1bc-40bd-854d-1b61dc96a5d1)

productivity matrix: 3 : User's commit productivity
user's commit productivity by considering the logarithmic ratio of additions and deletions to the total number of commits
measure of the complexity or impact of a user's code changes.
![image](https://github.com/DevaniYasora/DEVELOPER_IQ/assets/64655854/011bc557-4949-4998-8fd6-ad286c6ca867)



**DEVELOPMENT ARCHITECTURE**

**Step 01: Developed an EKS Cluster:**
Refer below mentioned link to create EKS cluster
reference: https://archive.eksworkshop.com/010_introduction/

Number of nodes: 3
![image](https://github.com/DevaniYasora/DEVELOPER_IQ/assets/64655854/198a6416-6e5b-4097-b88a-d8f78f0a0130)


![image](https://github.com/DevaniYasora/DEVELOPER_IQ/assets/64655854/c947f2a8-dcdf-47a8-95f3-68ae0262f898)

**Step 02: Microservices:**

There are 3 main microservices developed under the project. 
Microservice 1- Extract data from GitHub
Microservice 2- Perform productivity calculations.
Microservice 3- Display final productivity values. 

![image](https://github.com/DevaniYasora/DEVELOPER_IQ/assets/64655854/2ebee5c0-fe0c-4075-8688-37a7253a38ab)

![image](https://github.com/DevaniYasora/DEVELOPER_IQ/assets/64655854/3a1bb674-e5a4-42bf-bbfe-68d7d15bf05b)



**Microservice 1- Extract data from GitHub**
Withing this microservice, main 3 processers are performing. 
i-	Extracting data from GitHub:
To calculate the productivity of each developer we need to identify the developers who are engaging with the provided repository. As user details, username and GitHub login ID is extracted as 1st step. 
Then extract number of additions, deletion and all commit details for each developer.
Finally extract issues created and issues comments (The developer's involvement is being assessed, covering issues they've initiated, including pull requests and common bug reports. Furthermore, we are examining the extent of the developer's engagement with open issues, which encompasses both pull request reviews and responses to reported bugs.)
![image](https://github.com/DevaniYasora/DEVELOPER_IQ/assets/64655854/63e44dce-5a84-495a-9efe-ece84348feb9)
 

ii-	Summarized collected data – productivity matrix: 1
This process is considered as the 1st productivity matrix because under this process, the system calculated each and every developer’s total commit addition, total commit deletions, total number of commits in weekly, monthly and yearly basis. Also, its summarize the number of issues created and issues comments for each developer for a weekly, monthly and yearly basis. From this score, we can get an raw idea about developers behavior.

iii-	Insert data to DynamoDB table.
After performing the 1st productivity calculation process, data is saving to a table in DynamoDB database. Before inserting data to the table, it is deleting all data in the tables.
 
![image](https://github.com/DevaniYasora/DEVELOPER_IQ/assets/64655854/54dfc2f2-b4d9-4313-b49b-88cd730b46c5)


**Microservice 2- Perform productivity calculations.**
In this microservice, there are main 3 processes. 
i- Extracting data from DynamoDB table (In 1st microservice, data is saved for this table)
After extracting data from the database, data is saved to variables accordingly. 

ii- Performing productivity calculation matrix 2 and 3

Matrix 1: Productivity Matrix 1 is calculated by combining the counts of comments and issues created by a developer. Reflects a user's productivity based on their interactions, such as comments and issues created, over different time intervals (weekly, monthly, and yearly). 

Equation: (for weekly) 
	pr1= float(comments_weekly) + float(issues_created_weekly)

The same equation is performed to calculate monthly and yearly productivity by changing parameters accordingly. 

Matrix 2: Reflects a user's commit productivity by considering the logarithmic ratio of additions and deletions to the total number of commits. This is a measure of the complexity or impact of a user's code changes.

Equation: (for weekly)
	pr2=log⁡〖[(a_(value_weekly )+ d_value_weekly)/(c_value_weekly)〗

a_value_weekly: Number of additions (additions to code).
d_value_weekly: Number of deletions (deletions from code).
c_value_weekly: Number of commits (total code commits).

The same equation is performed to calculate monthly and yearly productivity by changing parameters accordingly. 
These matrices aim to provide insights into different aspects of a contributor's activities, combining both communication-related contributions and code-related contributions.

ii- Inserting data to the target table in DynamoDB
After the calculation process is completed, required data is saving to the final target table in the DynamoDB database. Before inserting data to the table, it is deleting all data in the tables.
After the process completed, it will display a message:
![image](https://github.com/DevaniYasora/DEVELOPER_IQ/assets/64655854/c5d402f2-7e17-4305-a442-cad14ecfc39f)

**Microservice 3- Display final productivity values.**
In this microservice, data is extracted from the final target tale and display in a proper way in the web browser. 
![image](https://github.com/DevaniYasora/DEVELOPER_IQ/assets/64655854/1ee4ca5d-2ff8-4cc9-8d66-33d6c10b43ee)






