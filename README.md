# AI Agent Resume Writter ALPHA
# Make sure to review any outputted resumes before applying with them!

This is my first attempt at writing an ai agent to write a better resume for apply for jobs.

It uses Pydantic AI and Gemini 2.0 Flash. There are env variables setup for the thinking and non thinking model. Play with each as you like.

## Setup

### Create .env file
Copy `.env.example` and rename it to `.env`

### Get a Google AI Studio API Key.

Go to [Google AI Studio](https://aistudio.google.com/) and click Get API Key in the top left corner. Once you get an api key paste it into your `.env` replacing the xxxx's after `AI_RESUME_GOOGLE_API_KEY`

### Install UV
We use uv to manage our dependencies. Follow the directions here to install it. [UV Instructions](https://github.com/astral-sh/uv)

Uv will automatically install depdendencies for the project being run so you can just follow the instructions below to run the project.

### Markdown to PDF 
If you are using Vscode install Markdown PDF `https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf`. Once installed open settings and look for `markdown pdf: display header footer` and disable that. That will keep it from putting the filename in the header of each pdf page.

If you have a different tool you like to convert markdown to pdf feel free to use that.


## Generating a resume

This is setup to generate a resume from a resume you already have and for a specific job description. You can you a different resume for each job. 

In the root directory you will see a documents directory. Inside of that create a new directory for the company you want to apply to, for example microsoft.
Inside of that directory you will place your resume in pdf format and the job_description in a .txt file. Your directory structure should look something like this.
```
├── README.md
├── documents
│   ├── microsoft
│   │   ├── job_description.txt
│   │   └── resume.pdf
│   └── resume_template.md
├── main.py
├── pyproject.toml
└── uv.lock
```

You will see a resume_template.md. That is the base template that Gemini will use to attempt to format your resume output. You can modify this as you like but this is the base template it will use. 

The resume argument is not required if you name your resume resume.pdf

Open a terminal and run `make gen_resume company={company_name} resume={resume}` 

For the microsoft example it would be `make gen_resume company=microsoft`

Once it is done, it will generate an `output` folder under the company directory with a new resume in it.
Open this with a markdown previewer either in vscode or whatever tool you want and validate it looks correct. I am still working on getting it to parse the template correctly.

If you are using the thinking model `gemini-2.0-flash-thinking-exp-1219` it will put the plan at the top of the resume markdown file. You will need to remove that.
# REVIEW THE RESUME OUTPUT BEFORE APPLYING WITH IT

once you have it edited as you like if you choose to use the Vscode markdown extension open the command pallet and run Markdown PDF: Export(pdf). This will generate a temporary html page and then finally a pdf in the a directory under the company called `output`

```
├── README.md
├── documents
│   ├── microsoft
│   │   ├── job_description.txt
│   │   ├── output
│   │   │   └── resume.md
│   │   └── resume.pdf
│   └── resume_template.md
├── main.py
├── pyproject.toml
└── uv.lock
```