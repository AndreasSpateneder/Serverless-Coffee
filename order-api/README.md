# Order API

This is the order API to replace Amazon step function workflow.
## Structure
The API is written in Python using the Fastapi Framework. The most important endpoint is /order which implements the order journey step functions. It integrates with AWS DynamoDB and Eventbridge to communicate with the other components of the project.


To deploy, follow the steps below:

1. Build the docker image with the docker file provided
2. Push the docker image to a registry of your choice
3. Create a new ECS Cluster either Fargate or EC2 
4. Create a task in the Amazon Elastic Container Service with the container
5. Give the task an IAM role with permissions for dynamodb and aws eventbridge 