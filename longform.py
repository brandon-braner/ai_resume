import os
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.gemini import GeminiModel
from markitdown import MarkItDown
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

current_path = Path(__file__).parent

def get_resume(company_name: str):
    resume_path =  f"./documents/{company_name}/resume.md"
    if not os.path.exists(resume_path):
        resume_path = "./documents/resume.md"
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
            You are an expert resume writer for software developers and software leadership. 
            You will get a resume template in markdown. You will get a resume named that lists the jobs a person has done. 
            Each job has the company, position title, start and end date, location. 
            
            It will also have one or more options listed below it depending on the role being applied for. 

            Each option will have a line that looks like **Option [number]: Description of what kind of role it should be used for.**

            You are to take the appriorpriate option and turn it into 4+ bullet points highly related to the job listed as the job description.

            Original Resume:
            {original_resume}

            Job Description:
            {job_description}

            Resume Template:
            {template}

            Please provide a tailored resume that:
            - Follows the design provided in the resume template.
            - The Name of each company Should be bold and the same font and color as everything else
            - Right align dates [Start Date] - [End Date]
            - Keep each job to 4+  high quality bullets. If the job mentions a specific technology please incldue it in bullet points
            - Emphasizes relevant experience and skills
            - Only include skills in the skills section relevant to the job
            - Uses keywords from the job description
            - Follows professional resume formatting
            - Keep all of the information from the original resume such as dates, names addresses
            - Output should be just the resume, nothing else
            - Replace placeholders: Replace placeholders like [Your Full Name], [Location], [Email Address], etc., with the actual details.
            - Quantify achievements: Where possible, include metrics (e.g., "Improved X by Y%") to highlight the impact of the work.
            - If you are a thinking model do not output the plan into the markdown file.
            """

    company_output_folder = current_path / "documents" / company_name / "output"
    company_output_folder.mkdir(parents=True, exist_ok=True)

    with open(f"{company_output_folder}/prompt.txt", "w", encoding="utf-8") as file:
        file.write(system_prompt)
    
    model_name="gemini-2.0-flash-thinking-exp-1219"
    # model_name = os.environ.get("AI_RESUME_GEMINI_AI_MODEL", "gemini-2.0-flash-exp")    
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

    try:
        result = resume_agent.run_sync("Provide new resume")
    except Exception as e:
        print(e)
    # company_output_folder = current_path / "documents" / company_name / "output"
    # company_output_folder.mkdir(parents=True, exist_ok=True)

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