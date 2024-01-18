# AWS Lambda Auto Tagger

This script searches for resources without 2 specific tags in 2 AWS regions and tags them using the AWS SDK for Python (Boto3) with Resource Explorer in an either a Lambda Function or a script to be executed locally.

## Pre Requisites

You must have an AWS account, and have your default credentials and AWS Region configured as described in the AWS Tools and SDKs Shared Configuration and Credentials Reference Guide.
Python 3.6.0 or later

### Install packages

Depending on how you have Python installed and on your operating system, the commands to install and run might vary slightly. For example, on Windows, use py in place of python.

The requirements.txt file defines the two packages needed to run this Python script. To install the required packages, create a virtual environment by running the following:

`` python -m venv .venv ``

This creates a virtual environment folder named .venv. Each virtual environment contains an independent set of Python packages. Activate the virtual environment by running one of the following:

`` .venv\Scripts\activate `` # Windows
`` source .venv/bin/activate `` # Linux, macOS, or Unix

Install the packages by running the following command:

`` python -m pip install -r requirements.txt ``
This installs all of the packages listed in the requirements.txt file in the current folder.
