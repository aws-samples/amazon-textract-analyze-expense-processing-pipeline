"""
Author: Manish Chugh

Lambda function for Amazon Textract AnalyzeExpense to help analyze expenses.This
function listens to s3 event notifications of every image upload to source s3
bucket and generates textract analyze expense output in easily digestable .txt 
or any other output of your choice 
"""

import os
import boto3
from helper.helper import S3Helper
from textractprettyprinter.t_pretty_print_expense import get_string
from textractprettyprinter.t_pretty_print_expense import Textract_Expense_Pretty_Print, Pretty_Print_Table_Format

"""
Main method for image processing and pretty printing the AnalyzeExpense Response
"""
def lambda_handler(event, context):

    """
    Initiate boto3 client for Amazon Textract
    """
    textract = boto3.client(service_name='textract')

    """
    Fetch source bucket and object key names from s3 event notifications event
    """
    s3_source_bucket_name = event['detail']['requestParameters']['bucketName']
    s3_request_file_name = event['detail']['requestParameters']['key']
    
    """
    Fetch output s3 bucket name created cloud formation template, function will store textract output in this bucket
    """
    s3_output_bucket_name = os.environ['outputs3bucketname']

    """
    textract analyze_expense call to synchronously process image file
    """
    try:
        response = textract.analyze_expense(
            Document={
                'S3Object': {
                    'Bucket': s3_source_bucket_name,
                    'Name': s3_request_file_name
                }
            })
        
        """
        Pretty print textract analyze expense response. Valid values are - "csv",
        "plain","simple","github","grid","fancy_grid" ,"pipe","orgtbl","jira","presto",
        "pretty","psql","rst","mediawiki","moinmoin","youtrack","html","unsafehtml",
        "latex","latex_raw","latex_booktabs","latex_longtable","textile","tsv"
        """
        pretty_printed_string = get_string(textract_json=response, output_type=[Textract_Expense_Pretty_Print.SUMMARY, Textract_Expense_Pretty_Print.LINEITEMGROUPS], table_format=Pretty_Print_Table_Format.fancy_grid)
        
        """
        Save pretty print output to s3 output bucket. This code could be replaced to 
        send this output to storage service of your choice too.
        """
        S3Helper.writeToS3(pretty_printed_string, s3_output_bucket_name, s3_request_file_name+"-analyzeexpenseresponse.txt")
        return "200"

    except Exception as e_raise:
        print(e_raise)
        raise e_raise
