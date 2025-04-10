import boto3
import json
from datetime import datetime

patient_data = "{'patientInformation': {'name': 'Aryan Jack Hamonangan Simanjuntak', 'gender': 'Male', 'dateOfBirth': '11-Sep-2021', 'age': '2 years 3 months 27 days'}, 'diagnosis': {'admittingDiagnosis': 'Tonsilofaringitis', 'dischargeDiagnosis': 'Rinotonsilofaringitis akuta + Bronchial hyperreactivity', 'icd10Code': 'ICD-10 Diagnosis'}, 'medications': [{'name': 'SPORETIK SYRUP 100MG/5ML 30ML (LASA)', 'form': 'Powder for oral suspension', 'dailyDose': '2 times a day 2 mL', 'route': 'Oral', 'specialNotes': 'Antibiotik, Habiskan', 'quantity': 30}, {'name': 'VENTOLIN NEBULES 2.5MG (LASA)', 'form': 'Inhalation solution', 'dailyDose': '2 times a day 2.50 mL', 'route': 'Inhalation/Respiratory Nebulizer', 'specialNotes': None, 'quantity': 25}, {'name': 'PULMICORT RESPULES 0.25MG/ML IN 2ML (LASA)', 'form': 'Inhalation solution', 'dailyDose': '2 times a day 2 mL', 'route': 'Inhalation/Respiratory Nebulizer', 'specialNotes': None, 'quantity': 20}, {'name': 'EKSIPIEN', 'form': None, 'dailyDose': '3 times a day 1 sachet', 'route': 'Cough Medicine', 'specialNotes': None, 'quantity': 60}, {'name': 'ISPRINOL SYRUP 250MG/5ML 60ML', 'form': 'Syrup', 'dailyDose': '4 times a day 2.50 mL', 'route': 'Oral', 'specialNotes': 'Habiskan', 'quantity': 60}, {'name': 'RYVEL DROPS 10MG/ML 10ML', 'form': 'Oral drops', 'dailyDose': '2 times a day 0.25 mL', 'route': 'Oral', 'specialNotes': 'Obat Alergi', 'quantity': 10}]}"

s3_client = boto3.client("s3")
bucket_name = "ayy-textractt"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
file_name = f"medical record data/{timestamp}.json"

data_json = json.dumps(patient_data)

s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=data_json)

print(f"✅ JSON stored in S3: s3://{bucket_name}/{file_name}")
