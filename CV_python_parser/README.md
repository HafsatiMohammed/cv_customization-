# CV Parser

A Python script that parses JSON-like files from the `CV_json` folder and generates a custom LaTeX CV file using the `isso.tex` template.

## Features

- Reads Python dictionary files (with comments) from `CV_json` folder
- Generates a custom LaTeX file (`isso_custom.tex`) using the `isso.tex` template
- Handles all CV sections: profile, experience, skills, languages, interests, etc.
- Properly escapes LaTeX special characters
- Converts markdown-style formatting to LaTeX

## File Structure

```
CV_python_parser/
├── cv_parser.py      # Main parser class
├── run_parser.py     # Simple runner script
├── requirements.txt  # Dependencies (none required)
└── README.md        # This file

CV_json/              # Input JSON files
├── profile.json
├── Professional_experience.json
├── diplomas.json
├── hard_skills.json
├── soft_skills.json
├── languages.json
├── Interest.json
└── side_projects.json

CV_tex/               # LaTeX files
├── isso.tex         # Template file
├── isso_custom.tex  # Generated output file
├── altacv.cls       # LaTeX class
└── sample.bib       # Bibliography
```

## Usage

### Method 1: Using the runner script
```bash
cd CV_python_parser
python run_parser.py
```

### Method 2: Direct execution
```bash
cd CV_python_parser
python cv_parser.py
```

### Method 3: As a module
```python
from cv_parser import CVParser

parser = CVParser()
parser.run()
```

## Input Format

The parser expects Python dictionary files (not standard JSON) with the following structure:

### profile.json
```python
profile = {
    "name": "Your Name",
    "tagline": "Your Title",
    "contact": {
        "email": "email@example.com",
        "phone": "+1234567890",
        "location": "City, Country",
        "linkedin": "linkedin.com/in/yourprofile",
        "age": 30
    },
    "summary": "Your professional summary...",
    "objective": "Your career objective..."
}
```

### Professional_experience.json
```python
experiences = {
    "Job Title": {
        "company": "Company Name",
        "dates": "Jan 2020 - Present",
        "location": "City, Country",
        "highlights": [
            "Achievement 1 with **bold text**",
            "Achievement 2"
        ],
        "tags": ["Skill1", "Skill2"]
    }
}
```

### Other files follow similar patterns for:
- `diplomas.json` - Education information
- `hard_skills.json` - Technical skills
- `soft_skills.json` - Soft skills
- `languages.json` - Language proficiency
- `Interest.json` - Personal interests
- `side_projects.json` - Side projects

## Output

The parser generates `isso_custom.tex` in the `CV_tex` folder, which can be compiled with LaTeX to produce a PDF CV.

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Notes

- The parser handles Python-style comments (lines starting with `#`)
- It converts markdown-style bold text (`**text**`) to LaTeX (`\textbf{text}`)
- Special LaTeX characters are automatically escaped
- The template file (`isso.tex`) must exist in the `CV_tex` folder 