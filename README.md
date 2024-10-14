# AWS EC2 state Lambda-switcher via HTTP
This repository contains code for an AWS Lambda function that enables you to manage the state of an EC2 instance (start, stop, and check status) using simple HTTP requests, without requiring direct access to the AWS Management Console or IAM credentials on the client side. The function can be triggered through API Gateway, making it accessible via predefined routes for different actions.

**Functionality:**
 /start: Starts the EC2 instance if it's stopped.
 /stop: Stops the EC2 instance if it's running.
 /status: Returns the current status of the EC2 instance.

**Requirements:**
- AWS Lambda
- Boto3 for interacting with EC2
- Proper IAM role with EC2 access permissions
- API Gateway
