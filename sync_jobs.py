import os
from pyairtable import Api
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def sync_jobs():
    api_key = os.environ.get("AIRTABLE_API_KEY_ENV")
    base_id = os.environ.get("AIRTABLE_BASE_ID")
    table_name = os.environ.get("AIRTABLE_TABLE_NAME")

    if not all([api_key, base_id, table_name]):
        print(
            "Error: Missing Airtable environment variables. Ensure AIRTABLE_API_KEY_ENV, AIRTABLE_BASE_ID, and AIRTABLE_TABLE_NAME are set."
        )
        return

    api = Api(api_key)
    table = api.table(base_id, table_name)

    print(f"Fetching jobs from table '{table_name}'...")
    try:
        # Only fetch records where 'Synced' is not checked
        records = table.all(formula="NOT({Synced})")
    except Exception as e:
        print(f"Error fetching from Airtable: {e}")
        return

    documents_path = Path(__file__).parent / "documents"
    documents_path.mkdir(exist_ok=True)

    count = 0
    for record in records:
        fields = record.get("fields", {})

        # Try to find Company column
        company = (
            fields.get("Company") or fields.get("Company Name") or fields.get("Name")
        )

        # Try to find Job Description column
        job_description = (
            fields.get("Job Description")
            or fields.get("Description")
            or fields.get("JD")
        )

        if company and job_description:
            # Clean company name for folder naming
            # User convention seems to be lowercase, e.g., 'microsoft'
            folder_name = (
                str(company).strip().lower().replace(" ", "_").replace("/", "_")
            )

            company_folder = documents_path / folder_name
            company_folder.mkdir(exist_ok=True)

            jd_path = company_folder / "job_description.txt"
            with open(jd_path, "w", encoding="utf-8") as f:
                f.write(job_description)

            # Mark as synced in Airtable
            try:
                table.update(record["id"], {"Synced": True})
                print(f"Synced {company} -> {folder_name}/job_description.txt")
                count += 1
            except Exception as e:
                print(f"Failed to update 'Synced' status for {company}: {e}")
        else:
            # Intentionally verbose to help debug field names if they mismatch
            print(
                f"Skipping record {record.get('id')}: Missing 'Company' or 'Job Description'. Found keys: {list(fields.keys())}"
            )

    print(f"Sync complete. {count} jobs synced.")


if __name__ == "__main__":
    sync_jobs()
