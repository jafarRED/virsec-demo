import boto3
import time
import os
import json
import sys
import base64
from datetime import datetime

def lambda_handler(event, context):
    print(f"Event received at: {datetime.now()}")
    print(f"Received event: {event}")
    
    for record in event['records'].values():
        for r in record:
            # Decode the Base64 value
            decoded_value = base64.b64decode(r['value']).decode('utf-8')
            print(f"Decoded message: {decoded_value}")
    
    return 'success'