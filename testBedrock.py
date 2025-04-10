import boto3
import json
import re

cleaned_text = "YOUR_CLEANED_TEXT_TO_TEST"

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

summary = ask_gen_ai("summarize the patient's information, diagnosis (including the ICD-10 code), and medication information (name, amount, and cost) from the claim patient's retrieved data using this extracted text" + cleaned_text + "return only json format, without text")
print(summary)

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
print(structured_data)