import boto3
import time
import re
import json
from datetime import datetime

textract = boto3.client('textract', region_name="ap-southeast-1") 

def extract_text_from_pdf(s3_bucket, s3_file):
    response = textract.start_document_text_detection(
        DocumentLocation={'S3Object': {'Bucket': s3_bucket, 'Name': s3_file}}
    )
    job_id = response['JobId']
    print(f"Started text extraction job: {job_id}")

    while True:
        result = textract.get_document_text_detection(JobId=job_id)
        status = result['JobStatus']
        if status in ['SUCCEEDED', 'FAILED']:
            break
        print("Waiting for job to complete...")
        time.sleep(5)

    if status == "SUCCEEDED":
        extracted_text = ""
        next_token = None

        while True:
            if next_token:
                result = textract.get_document_text_detection(
                    JobId=job_id, NextToken=next_token
                )
            for block in result["Blocks"]:
                if block["BlockType"] == "LINE":
                    extracted_text += block["Text"] + "\n"
            next_token = result.get("NextToken")
            if not next_token:
                break
        return extracted_text
    else:
        print("Text extraction failed!")
        return None

s3_bucket = "ayy-textractt"
s3_file = input("Enter your s3 filename: ")
extracted_text = extract_text_from_pdf(s3_bucket, s3_file)

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

cleaned_text = clean_text(extracted_text)

bedrock = boto3.client('bedrock-runtime', region_name="ap-southeast-1")
def ask_gen_ai(prompt):
    try:
        response = bedrock.invoke_model(
            modelId="apac.anthropic.claude-3-sonnet-20240229-v1:0",
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 200000
            })
        )
        response_data = json.loads(response["body"].read().decode())
        return response_data
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

summary = ask_gen_ai("summarize the patient's information, diagnosis (including the ICD-10 code), and medication information (name, amount, and cost) \nfrom the claim patient's retrieved data using this extracted text\n" + cleaned_text + "\nreturn only json format, without text")
#print(summary)

def extract_json_from_claude(response_data):
    """
    Extracts a valid JSON object from Claude's response.
    """
    try:
        content_text = response_data.get("content", [{}])[0].get("text", "")
        
        json_match = re.search(r"\{.*\}", content_text, re.DOTALL)
        
        if json_match:
            json_str = json_match.group() 
            
            try:
                cleaned_json = json.loads(json_str)
                return cleaned_json 
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON decoding error: {e}")
                print("Raw Extracted JSON:", json_str)
                return None
        else:
            print("❌ No JSON found in response.")
            print("Full Response Text:", content_text) 
            return None
    except Exception as e:
        print(f"❌ Error extracting JSON: {e}")
        return None

structured_data = extract_json_from_claude(summary)
#print(structured_data)

s3_client = boto3.client("s3")
bucket_name = "ayy-textractt"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
file_name = f"medical record data/{timestamp}.json"

data_json = json.dumps(structured_data)

s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=data_json)

print(f"✅ JSON stored in S3: s3://{bucket_name}/{file_name}")