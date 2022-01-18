#----------------------------------------------------------------
### Lambda Function 1
import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    # Get the s3 address from the Step Function event input
    key = event['s3_key']## TODO: fill in
    bucket = event['s3_bucket']## TODO: fill in

    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    s3.download_file(bucket,key,"/tmp/image.png")
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

#---------------------------------------------------------------
#Lambda 2 function



import boto3
import json
import base64

runtime = boto3.client('runtime.sagemaker')

# Fill this in with the name of your deployed model
ENDPOINT = 'image-classification-2022-01-14-09-15-43-624'



## TODO: fill in


def lambda_handler(event, context):
    
    
    image = base64.b64decode(event['body']["image_data"])
    
   
    
   
    response = runtime.invoke_endpoint (EndpointName=ENDPOINT, 
                ContentType='image/png',                                        
                Body=image)
                
    

    
    
    inferences = json.loads(response['Body'].read())
    
    #event["inferences"] = response.decode('utf-8')
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

#----------------------------------------------------------------------------------------
#3rd lambda function
import json


THRESHOLD = .93


def lambda_handler(event, context):

    #inferences = [0.22, 0.99]
    # Grab the inferences from the event
    inferences = event['inferences'] ## TODO: fill in
    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = any(x > THRESHOLD for x in inferences) ## TODO: fill in
    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }