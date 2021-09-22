# Synchronously process your receipt and invoice images using Amazon Textract AnalyzeExpense


## Introduction
Receipts and invoices are special types of documents that are critical to small, medium businesses (SMBs), startups, and enterprises for managing their accounts payable process. These types of documents are difficult to process at scale because they follow no set design rules, yet any individual customer encounters thousands of distinct types of these documents. In this sample, you can use Amazon Textract to extract data from any invoice or receipt (in English) without any required machine learning (ML) experience or templates or configuration. Amazon Textract extracts a set of standard fields and related line-item details from your receipts and this solution provide pretty printing capabilities to output this data in various formats including .csv, txt and others.

## Architecture

![architecture](architecture.png)

At a high level, the solution architecture includes the following steps:
1.	Sets up an Amazon S3 source and output buckets storing raw expense documents images in png, jpg(jpeg) formats.
2.	Configures an Event Rule based on event pattern in Amazon EventBridge to match incoming S3 PutObject events in the S3 folder containing the raw expense document images.
3.	Configured EventBridge Event Rule sends the event to an AWS Lambda function for futher analysis and processing.
4.	AWS Lambda function reads the images from Amazon S3, calls Amazon Textract AnalyzeExpense API, uses Amazon Textract Response Parser to de-serialize the JSON response and uses Amazon Textract PrettyPrinter to easily print the parsed response and stores the results back to Amazon S3 in different formats.

## Prerequisites
1. python
2. AWS CLI

## Deployment

Two ways you could deploy this solution

### Option 1 - Custom deployment
1. Download this git repo on your local machine
2. Install Amazon Textract Pretty Printer and Response Parser
```
cd amazon-textract-analyzeexpense

python -m pip install --target=./ amazon-textract-response-parser

python -m pip install --target=./ amazon-textract-prettyprinter
```
3. Create lambda function deployment package (.zip) file
```
zip -r archive.zip .
```
4. Next, copy archive.zip file to a s3 bucket of your choice.
```
aws s3 cp archive.zip s3://my-source-bucket
```
If you need to create a new bucket in us-east-1
>`aws s3api create-bucket --bucket my-source-bucket --region us-east-1`
>
And, for all other regions, add `--create-bucket-configuration` option
>`aws s3api create-bucket --bucket my-source-bucket --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2`

5. Open template.yaml file, replace s3 bucket name under "EventConsumerFunction:" section with your s3 bucket name, and save.
6. Finally, deploy this solution
```
aws cloudformation deploy --template-file template.yaml --stack-name myTextractAnalyzeExpense --capabilities CAPABILITY_NAMED_IAM
```


### Option 2 - Auto deploy using cloudformation template
Alternatively, deploy this solution in `us-east-1` using a pre-configured CloudFormation template -
1.	Choose Launch Stack to configure the notebook in the US East (N. Virginia) Region:

[![cfnlaunchstack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=textract-analyzexpense&templateURL=https://aws-ml-blog.s3.amazonaws.com/artifacts/analyze-expense-documents-textract/Textract-Analyze-Expense-Demo.yaml)

2. Don’t make any changes to stack name or parameters.
3. In the Capabilities section, select I acknowledge that AWS CloudFormation might create IAM resources.
4. Choose Create stack.

## Test
In order to test the solution, upload the receipts/invoice images in the Amazon S3 bucket created by CloudFormation template. This will trigger an event to invoke AWS Lambda function which will call the Amazon Textract AnalyzeExpense API, parse the response JSON, convert the parsed response into csv format and store it back to the same Amazon S3 Bucket. You can extend the provided AWS Lambda function further based on your requirements and also change the output format to other types like tsv, grid, latex and many more by setting the appropriate value of output_type when calling get_string method of textractprettyprinter.t_pretty_print_expense in Amazon Textract PrettyPrinter.

## Clean up

Deleting the CloudFormation Stack will remove the Lambda functions, EventBridge rules and other resources created by this solution. Ensure the S3 buckets are empty before attempting to delete this stack.

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.
