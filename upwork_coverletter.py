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
    job_description_path = company_folder / "jd.txt"
    with open(job_description_path, "r") as file:
        return file.read()

def get_custom_prompt(company_name):
    company_folder = current_path / "documents" / company_name
    company_folder.mkdir(parents=True, exist_ok=True)
    custom_prompt_path = company_folder / "cp.txt"
    if os.path.exists(custom_prompt_path):
        with open(custom_prompt_path, "r") as file:
            return file.read()
    return ""
    

def main(company_name: str, resume_name: str):
    original_resume = get_resume(company_name)
    job_description = get_job_description_local(company_name)
    template = get_template()
    custom_prompt = get_custom_prompt(company_name)

    system_prompt = f"""
            You are an expert upwork coverletter writer for software developers and software leadership. 
            You will get a resume template in markdown. You will get a resume named that lists the jobs a person has done. 
            Each job has the company, position title, start and end date, location. 
             
            Original Resume:
            {original_resume}

            Job Description:
            {job_description}

            Proposal Template: 
            Hi [Client Name],  

            I’m excited to apply for the [Job Title] role. With [X] years of experience [briefly summarize your niche, e.g., "leading engineering teams to build scalable SaaS platforms"], I’ve consistently delivered results for organizations like [Client’s Industry/Similar Companies]. Here’s how I can address your needs:  

**Why I’m a Fit:**  
- ✅ **Expertise in [Key Requirement 1]:** At [Previous Company], I [achievement tied to requirement]. For example, [specific metric/story].  
- ✅ **Proven Success with [Key Requirement 2]:** Led [project/initiative] using [tool/technology], resulting in [quantifiable outcome].  
- ✅ **Certifications/Education:** [Mention relevant certs, e.g., "Google Cloud Architect"] + [Degree, if applicable].  

**Relevant Achievements:**  
- 🚀 [Achievement 1]: [Impact, e.g., "Scaled a warehouse management system to handle 2M+ daily transactions"].  
- 📈 [Achievement 2]: [Result, e.g., "Reduced onboarding errors by 60% via event-driven architecture"].  
- ⚡ [Achievement 3]: [Efficiency gain, e.g., "Cut deployment cycles from monthly to daily with CI/CD pipelines"].  

**What I Offer:**  
- **Hands-On Execution:** Deep technical skills in [tools] to ensure rapid, high-quality delivery.  
- **Agile Innovation:** Passion for solving complex problems like [mention a pain point from their job post].  

I’d love to discuss how my experience can drive similar results for [Client’s Project/Company]. Let’s schedule a call to explore your vision!  

Best regards,  
[Your Name]  
[Portfolio/Website] | [LinkedIn] | [Calendly Link (if applicable)] 
            
            For this specific job also follow the rules set forth below
            {custom_prompt}

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