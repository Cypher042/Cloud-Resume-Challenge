import azure.functions as func
import logging
import os
import json
from azure.cosmos import CosmosClient, exceptions

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

COSMOS_URL = os.environ.get("COSMOS_URL")
COSMOS_KEY = os.environ.get("COSMOS_KEY")
DATABASE_NAME = "cypher-cloud-resume-db"
CONTAINER_NAME = "counter"

def get_cosmos_client():
    return CosmosClient(COSMOS_URL, COSMOS_KEY)

@app.route(route="getResumeCounter", methods=["GET"])
def getResumeCounter(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Getting resume counter from Cosmos DB.')
    
    try:

        client = get_cosmos_client()
        database = client.get_database_client(DATABASE_NAME)
        container = database.get_container_client(CONTAINER_NAME)
        
        counter_id = "1"
        
        try:
            counter_doc = container.read_item(item=counter_id, partition_key=counter_id)
            count = counter_doc.get("count", 0)
            
            counter_doc["count"] = count + 1
            
            container.replace_item(item=counter_id, body=counter_doc)
            
            return func.HttpResponse(
                json.dumps({
                    "id": counter_doc["id"],
                    "count": counter_doc["count"]
                }),
                status_code=200,
                headers={
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type"
                }
            )
            
        except exceptions.CosmosResourceNotFoundError:
            new_counter = {
                "id": "1",
                "count": 1
            }
            container.create_item(body=new_counter)
            
            return func.HttpResponse(
                json.dumps({
                    "id": "1",
                    "count": 1
                }),
                status_code=200,
                headers={
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type"
                }
            )
            
    except Exception as e:
        logging.error(f"Error accessing Cosmos DB: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "error": "Failed to retrieve counter",
                "message": str(e)
            }),
            status_code=500,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        )

@app.route(route="getResumeCounter", methods=["OPTIONS"])
def handle_options(req: func.HttpRequest) -> func.HttpResponse:
    """Handle CORS preflight requests"""
    return func.HttpResponse(
        "",
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }
    )