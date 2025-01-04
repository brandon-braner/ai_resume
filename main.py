import os
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.gemini import GeminiModel
from markitdown import MarkItDown
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

current_path = Path(__file__).parent

def get_resume(company_name: str):
    resume_path =  f"./documents/{company_name}/resume.pdf"
    md = MarkItDown()
    return md.convert(resume_path).text_content

def get_template():
    template_path = "./documents/resume_template.md"
    md = MarkItDown()
    return md.convert(template_path).text_content

def get_job_description_local(company_name):
    company_folder = current_path / "documents" / company_name
    company_folder.mkdir(parents=True, exist_ok=True)
    job_description_path = company_folder / "job_description.txt"
    with open(job_description_path, "r") as file:
        return file.read()
    
    

def main(company_name: str, resume_name: str):
    original_resume = get_resume(company_name)
    job_description = get_job_description_local(company_name)
    template = get_template()

    system_prompt = f"""
            As an expert resume writer, analyze the following original resume and job description,
            then create a tailored version of the resume that highlights relevant experience and skills
            for the specific job. Keep all the original resume content and adjust the responsibilites to fit the job.
            Please follow the template provided for the output.

            Original Resume:
            {original_resume}

            Job Description:
            {job_description}

            Template:
            {template}

            Please provide a tailored resume that:
            - The Name of each company Should be bold and the same font and color as everything else
            - Right align dates [Start Date] - [End Date]
            - Keep each job to 3 or 4  high quality bullets
            - Emphasizes relevant experience and skills
            - Uses keywords from the job description
            - Follows professional resume formatting
            - Keep all of the information from the original resume such as dates, names addresses
            - Output should be just the resume, nothing else
            - Replace placeholders: Replace placeholders like [Your Full Name], [Location], [Email Address], etc., with the actual details.
            - Quantify achievements: Where possible, include metrics (e.g., "Improved X by Y%") to highlight the impact of your work.
            - If you are a thinking model do not output the plan into the markdown file.
            """

    model_name = os.environ.get("AI_RESUME_GEMINI_AI_MODEL", "gemini-2.0-flash-exp")    
    api_key = os.environ.get("AI_RESUME_GOOGLE_API_KEY")
    model = GeminiModel(
        model_name,
        api_key=api_key,
    )
    resume_agent = Agent(
        model=model,
        result_type=str,
        system_prompt=system_prompt,
    )

    result = resume_agent.run_sync("Provide new resume following the bullets above")

    company_output_folder = current_path / "documents" / company_name / "output"
    company_output_folder.mkdir(parents=True, exist_ok=True)

    resume_name_without_extension = os.path.splitext(resume_name)[0]
    

    output_path = company_output_folder / f"{resume_name_without_extension}.md"

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(result.data)
    

 
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", help="Company name", required=True)
    parser.add_argument("--resume", help="Resume name", required=True)
    args = parser.parse_args()
    main(company_name=args.company, resume_name=args.resume)