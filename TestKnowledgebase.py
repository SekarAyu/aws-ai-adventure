import boto3
import time

kb_client = boto3.client("bedrock-agent")

knowledge_base_id = "YOUR_KNOWLEDGEBASE_ID" 
data_source_id = "YOUR_DATA_SOURCE_ID" 

response = kb_client.start_ingestion_job(
    knowledgeBaseId=knowledge_base_id,
    dataSourceId=data_source_id
)

job_id = response["ingestionJob"]["ingestionJobId"]

while True:
    status_response = kb_client.get_ingestion_job(
        knowledgeBaseId=knowledge_base_id,
        dataSourceId=data_source_id,
        ingestionJobId=job_id
    )

    status = status_response["ingestionJob"]["status"]
    print(f"Current Status: {status}")

    if status in ["COMPLETE", "FAILED"]:
        break

    time.sleep(10)

print("Final Status:", status)
