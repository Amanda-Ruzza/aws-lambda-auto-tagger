"""
Purpose

Searches for resources without 2 specific tags and tags them using the AWS SDK for Python (Boto3) with Resource Explorer in an either a Lambda Function or a script to be executed locally.
"""


import boto3
from botocore.exceptions  import ClientError
from botocore.config import Config
import logging
import json


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)


def lambda_handler(event, context):
    logger.debug('Incoming Event')
    logger.debug(event)
    
    resource_explorer_client = boto3.client(
        'resource-explorer-2',
    )
     
    missing_philosophy_tag = get_resources_missing_tag(resource_explorer_client, 'philosophy')
    missing_liberal_arts_tag = get_resources_missing_tag(resource_explorer_client, 'liberal-arts')
    
    logger.info(f"# of Resources Missing 'philosophy' {missing_philosophy_tag['Count']['TotalResources']} - Complete List? {missing_philosophy_tag['Count']['Complete']}")
    logger.info(f"# of Resources Missing 'liberal-arts' {missing_liberal_arts_tag['Count']['TotalResources']} - Complete List? {missing_liberal_arts_tag['Count']['Complete']}")
    
    map_philosophy_arns=[]
    for this_resource in missing_philosophy_tag['Resources']:
        map_philosophy_arns.append(this_resource['Arn'])
    logger.info(f"The Map Philosophy ARN:{map_philosophy_arns}")
    
    map_liberal_arts_arns=[]
    for this_resource in missing_liberal_arts_tag['Resources']:
        map_liberal_arts_arns.append(this_resource['Arn'])
    logger.info(f"The Map Liberal Arts ARN:{map_liberal_arts_arns}")
       
    apply_tags(map_philosophy_arns, {'philosophy': 'phil-dept-server'})
   
    apply_tags(map_liberal_arts_arns, {'liberal-arts': 'la-dept-server'})
    

def get_resources_missing_tag(client, tag_name): #Resource Explorer will only give me 100 results per time, however, since we're running a Lambda, it doesn't matter
    return (
        client.get_paginator('search')
            .paginate(QueryString=f"-tag.key:{tag_name}")
            .build_full_result()
    )
def apply_tags(list_of_resources, tag_map):
    resources_by_region = return_resources_by_region(list_of_resources)
    counter = 0
    for this_resource in list_of_resources:
        counter += 1
        logger.info(f"{counter}) Add tag '{tag_map.keys()}' to '{this_resource}'")
    # iterates over regions:
    regions = ['us-east-1', 'us-east-2']
    for region in regions: 
        tagging_client = boto3.client('resourcegroupstaggingapi', region_name=region)
        
    # create a 'for loop' that slices 19 elements from the  resources list before sending them to be tagged 
        start = 0
        end = 20
        while start < len(resources_by_region[region]):
            sliced_list = resources_by_region[region][start : end]
            start = end
            end += 20
            logger.debug(len(sliced_list))
            # Adding a print statement to the main list before the 2 regional filters:
            logger.info(f"The PAGINATED Resources in the 'new_list' are: \n {sliced_list} \n")
   
            try:
                response = tagging_client.tag_resources(
                    ResourceARNList=sliced_list,
                    Tags=tag_map
                )
                logger.info(response)
            except ClientError as e:       
                logger.info(f"Attempted to Tag this resource, however it's no longer available. \n {e}")
            continue

def return_resources_by_region(resources_for_all_regions):
    resources_by_region = dict()
    regions = ['us-east-1', 'us-east-2']
    for region_name in regions:
        resources_by_region[region_name] = [arn for arn in resources_for_all_regions if region_name in arn]
    
        logger.info(f"The {region_name} resources are: \n {resources_by_region[region_name]} \n") 

    return resources_by_region
    
def format_in_json(response):
    return json.dumps(response, indent=4, sort_keys=True, default=str)
    
if __name__ == '__main__':
    lambda_handler(None, None)