import boto3,json,os
from boto3 import session
from ec2_metadata import ec2_metadata
from flask import Flask
from flask import Flask, render_template
app = Flask(__name__)

RegionName = ec2_metadata.region
dynamodb = boto3.resource('dynamodb',region_name=RegionName)
#dynamodb = boto3.resource('dynamodb',region_name=os.environ['AWS_REGION'])

fopen = open("/etc/environment", "r")
for x in fopen:
    print(x)
    TableName = x.split("=")[-1].replace("\n", "").strip()
    print(TableName)
table=dynamodb.Table(TableName)

@app.route("/")
def index():
    items = [
        {'id': "0",
         'name': 'Pipeline',
         'description': 'CodeBuild Pipeline',
         'image': 'pipeline.png'},
        {'id': "1",
         'name': 'ImageBuild',
         'description': 'Ami Build',
         'image': 'imagebuild.png'}
    ]
    for i in items:
        table.put_item(Item=i)
    return render_template('demo.html', name=items)
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
