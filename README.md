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

**Step 01: Developed an EKS Cluster:**
Refer below mentioned link to create EKS cluster
reference: https://archive.eksworkshop.com/010_introduction/

Number of nodes: 3
![image](https://github.com/DevaniYasora/DEVELOPER_IQ/assets/64655854/198a6416-6e5b-4097-b88a-d8f78f0a0130)


