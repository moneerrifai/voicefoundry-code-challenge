import os
import boto3
from botocore.config import Config
import logging
import json

# set retries 
config = Config(retries = {'max_attempts': 10})

api_id = os.environ['api_id']
website_bucket = os.environ['website_bucket']
region = os.environ['region']
stage = os.environ['stage']

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s')

# Suppress boto3 logging
logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)

index_html_contents = f'''
    <html>
        <head>
            <link rel="stylesheet" type="text/css" href="main.css">
            <script>
                function addPointsFunction() {{
                    var payload = {{
                    "input": JSON.stringify({{
                            description: document.getElementById('description').value,
                            points: document.getElementById('points').value,
                            date: document.getElementById('date').value
                    }})
                }}   
                console.log(JSON.stringify(payload))
                var xhttp = new XMLHttpRequest();
                xhttp.open("POST", "https://{api_id}.execute-api.{region}.amazonaws.com/{stage}/points", true);
                xhttp.send(JSON.stringify(payload))
                document.getElementById('submit').style.display = "none";
                document.getElementById('thankyou').style.display = "inline";
                }}

                
            </script>
        </head>
        <body>
        <div class="container">
            <h1>Welcome to the Moneer's Husband Points Portal</h1>
        <form id="submit">
            <h3>Add Husband Points</h3>
            <h4>What awesome thing did your husband just do? Please enter a description and a fair number of points</h4>
            <fieldset>
            <input id="description" name="description" placeholder="Description of your husband's amazing actions" type="text" tabindex="1" required autofocus>
            </fieldset>
            <fieldset>
            <input id="points" name="points "placeholder="Number of points awarded" type="text" tabindex="2" required>
            </fieldset>
            <fieldset>
                <input id="date" name="date" placeholder="Date of event" type="date" tabindex="5" required>
            </fieldset>
            <fieldset>
            <button type="button" name="points-submit" onclick="javascript:addPointsFunction()" id="points-submit" data-submit="...Sending">Add husband points</button>
            </fieldset>
            </form>

            <p class="copyright">Created by Moneer Rifai</p>
            
            <h1 id="thankyou">
                <br>
                <br>
                <br>
                <br>
                <br>
                Thank you for using Moneer's Husband Point Dashboard! Go to <a href="./index.html">homepage</a>.
            </h1>        
        </div>
        </body>
        </html>
'''

def lambda_handler(event, context):

    # this lambda function creates a static HTML site, and references the API Gateway ID that gets created upon deploy

    # log event
    logger.info(json.dumps(event))

    # create s3 client 
    s3_client = boto3.client('s3', config=config)

    # create file
    with open('/tmp/index.html', 'w') as file:
        file.write(index_html_contents)

    # upload file to S3 bucket
    s3_client.upload_file('/tmp/index.html',website_bucket, 'index.html', ExtraArgs={'ContentType':'text/html'})

    return 'index.html successfully uploaded to S3'