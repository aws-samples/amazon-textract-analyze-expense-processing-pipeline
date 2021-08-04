"""
Author: Manish Chugh

Helper file to assist with AWS and S3 reusable functions
"""
import boto3
from botocore.client import Config

class AWSHelper:

    def getResource(self, name, awsRegion=None):
        config = Config(
            retries = dict(
                max_attempts = 30
            )
        )

        if(awsRegion):
            return boto3.resource(name, region_name=awsRegion, config=config)
        else:
            return boto3.resource(name, config=config)
            
class S3Helper:

    @staticmethod
    def writeToS3(content, bucketName, s3FileName, awsRegion=None):
        s3 = AWSHelper().getResource('s3', awsRegion)
        object = s3.Object(bucketName, s3FileName)
        object.put(Body=content)
