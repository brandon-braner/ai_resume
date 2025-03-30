import requests
import os
from dotenv import load_dotenv
import pathlib
import re
import json

# Load environment variables
load_dotenv(override=True)

# Get Airtable credentials from environment variables
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY_ENV')
print("AIRTABLE API KEY: ", AIRTABLE_API_KEY)
BASE_ID = os.getenv('AIRTABLE_BASE_ID', 'app27SuqvQaEsN7Mu')
TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME', 'Jobs')

def sanitize_filename(filename:str):
    # Remove or replace invalid characters
    filename = filename.lower()
    return re.sub(r'[<>:"/\\|?*\s]', '_', filename)


def update_record_synced(record_id):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "records": [
            {
                "id": record_id,
                "fields": {
                    "Synced": True
                }
            }
        ]
    }
    
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    print(f"Updated record {record_id} as synced")

def create_company_folder(company_name, job_description):
    # Create base documents directory if it doesn't exist
    base_path = pathlib.Path('documents')
    base_path.mkdir(parents=True, exist_ok=True)
    
    # Sanitize company name for folder name
    safe_company_name = sanitize_filename(company_name)
    
    # Create company directory
    company_path = base_path / safe_company_name
    company_path.mkdir(exist_ok=True)
    
    # Create and write to jd.txt
    jd_file = company_path / 'jd.txt'
    jd_file.write_text(job_description)
    
    print(f"Created folder and JD file for {company_name}")
    return True

def query_airtable():
    try:
        url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
        
        headers = {
            "Authorization": f"Bearer {AIRTABLE_API_KEY}"
        }
        
        params = {
            "sort[0][field]": "Created At",
            "sort[0][direction]": "desc",
            "filterByFormula": "AND(Status='Not Applied', NOT({Synced}))"  # Only get unsynced records
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        print(data)
        
        # Process records and create folders/files
        for record in data.get('records', []):
            record_id = record['id']
            fields = record['fields']
            company_name = fields.get('Company Name')
            job_description = fields.get('Job Description', '')
            
            if company_name:
                # Create the folder and file
                success = create_company_folder(company_name, job_description)
                if success:
                    print(f"Record ID: {record_id}")
                    print("-" * 50)
                    # Update the record as synced in Airtable
                    update_record_synced(record_id)

        return data

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    query_airtable()
