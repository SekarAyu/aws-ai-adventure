import boto3
import time
import re

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
#s3_file = "2401080019.pdf"
extracted_text = extract_text_from_pdf(s3_bucket, s3_file)
print(extracted_text)

# def clean_text(text):
#     text = re.sub(r'\s+', ' ', text)
#     text = text.strip()
#     return text

# cleaned_text = clean_text(extracted_text)
# print(cleaned_text)