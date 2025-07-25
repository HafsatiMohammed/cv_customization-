#!/usr/bin/env python3
"""
Simple CV Parser - Uses basic string operations
Reads JSON files from CV_json folder and generates isso_custom.tex using isso.tex template
"""

import os
import re
import ast
from pathlib import Path
from typing import Dict, List, Any


class SimpleCVParser:
    def __init__(self, json_dir: str = "../CV_json", tex_dir: str = "../CV_tex"):
        """Initialize the parser with directories"""
        self.json_dir = Path(json_dir)
        self.tex_dir = Path(tex_dir)
        self.output_file = self.tex_dir / "isso_custom.tex"
        
        # Data storage
        self.profile = {}
        self.experience = {}
        self.diplomas = {}
        self.languages = {}
        self.hard_skills = {}
        self.soft_skills = {}
        self.interests = {}
        self.side_projects = {}
        
    def load_python_dict_file(self, filepath: Path) -> Dict[str, Any]:
        """Load a Python dictionary from a file (handles comments and non-standard JSON)"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove comments (lines starting with #)
            lines = content.split('\n')
            cleaned_lines = []
            for line in lines:
                if not line.strip().startswith('#'):
                    cleaned_lines.append(line)
            
            cleaned_content = '\n'.join(cleaned_lines)
            
            # Fix common syntax issues
            # Fix missing commas in lists
            cleaned_content = re.sub(r'(\w+)"\s*\n\s*"', r'\1",\n        "', cleaned_content)
            # Fix missing quotes around strings
            cleaned_content = re.sub(r'(\w+)"\s*/\s*"(\w+)"', r'\1", "\2"', cleaned_content)
            # Fix missing commas after strings in lists
            cleaned_content = re.sub(r'"([^"]+)"\s*\n\s*"([^"]+)"', r'"\1",\n        "\2"', cleaned_content)
            
            # Find the dictionary assignment (e.g., "profile = {...}")
            match = re.search(r'(\w+)\s*=\s*({.*})', cleaned_content, re.DOTALL)
            if match:
                dict_content = match.group(2)
                # Safely evaluate the dictionary
                result = ast.literal_eval(dict_content)
                
                # Convert tuple strings to regular strings
                if isinstance(result, dict):
                    for key, value in result.items():
                        if isinstance(value, tuple):
                            # Join tuple strings into a single string
                            result[key] = ''.join(str(item) for item in value)
                
                return result
            else:
                raise ValueError(f"Could not find dictionary assignment in {filepath}")
                
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return {}
    
    def load_all_data(self):
        """Load all JSON files into memory"""
        print("Loading CV data from JSON files...")
        
        # Load profile data
        profile_file = self.json_dir / "profile.json"
        if profile_file.exists():
            self.profile = self.load_python_dict_file(profile_file)
        
        # Load professional experience
        exp_file = self.json_dir / "Professional_experience.json"
        if exp_file.exists():
            self.experiences = self.load_python_dict_file(exp_file)
        
        # Load diplomas
        diplomas_file = self.json_dir / "diplomas.json"
        if diplomas_file.exists():
            self.diplomas = self.load_python_dict_file(diplomas_file)
        
        # Load hard skills
        hard_skills_file = self.json_dir / "hard_skills.json"
        if hard_skills_file.exists():
            self.hard_skills = self.load_python_dict_file(hard_skills_file)
        
        # Load soft skills
        soft_skills_file = self.json_dir / "soft_skills.json"
        if soft_skills_file.exists():
            self.soft_skills = self.load_python_dict_file(soft_skills_file)
        
        # Load languages
        languages_file = self.json_dir / "languages.json"
        if languages_file.exists():
            self.languages = self.load_python_dict_file(languages_file)
        
        # Load interests
        interests_file = self.json_dir / "Interest.json"
        if interests_file.exists():
            self.interests = self.load_python_dict_file(interests_file)
        
        # Load side projects
        side_projects_file = self.json_dir / "side_projects.json"
        if side_projects_file.exists():
            self.side_projects = self.load_python_dict_file(side_projects_file)
        
        print("Data loading completed!")
    
    def escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters with minimal processing"""
        if not isinstance(text, str):
            return str(text)
        
        # Don't escape if the text already contains LaTeX commands
        if '\\' in text and any(cmd in text for cmd in ['\\textbar{}', '\\textbf{', '\\textcolor{', '\\cvtag{', '\\cvevent{', '\\href{', '\\faExternalLink', '\\faMortarBoard', '\\vspace{', '\\cvsection{', '\\begin{', '\\end{', '\\item', '\\switchcolumn', '\\newpage']):
            # This is already LaTeX formatted, just escape basic characters
            text = text.replace('_', r'\_')
            text = text.replace('^', r'\^{}')
            text = text.replace('~', r'\textasciitilde{}')
            text = text.replace('$', r'\$')
            text = text.replace('%', r'\%')
            text = text.replace('#', r'\#')
            text = text.replace('&', r'\&')
            return text
        
        # Handle basic LaTeX special characters for plain text
        text = text.replace('\\', r'\textbackslash{}')
        text = text.replace('{', r'\{')
        text = text.replace('}', r'\}')
        text = text.replace('_', r'\_')
        text = text.replace('^', r'\^{}')
        text = text.replace('~', r'\textasciitilde{}')
        text = text.replace('$', r'\$')
        text = text.replace('#', r'\#')
        text = text.replace('&', r'\&')
        text = text.replace('%', r'\%')
        
        return text
    
    def format_contact_info(self) -> str:
        """Format contact information for LaTeX"""
        if not self.profile or 'contact' not in self.profile:
            return ""
        
        contact = self.profile['contact']
        lines = []
        
        if 'email' in contact:
            lines.append(f"\\email{{{self.escape_latex(contact['email'])}}}")
        if 'phone' in contact:
            lines.append(f"\\phone{{{self.escape_latex(contact['phone'])}}}")
        if 'location' in contact:
            lines.append(f"\\location{{{self.escape_latex(contact['location'])}}}")
        if 'linkedin' in contact:
            lines.append(f"\\linkedin{{{self.escape_latex(contact['linkedin'])}}}")
        if 'age' in contact:
            lines.append(f"\\textbf{{Age}}: {contact['age']}")
        
        return '\n    '.join(lines)
    
    def format_experience_section(self) -> str:
        """Format experience section with optimized spacing"""
        if not self.experiences:
            return ""
        
        sections = []
        for i, (job_id, data) in enumerate(self.experiences.items()):
            title = data.get('title', job_id)
            company = data.get('company', '')
            dates = data.get('dates', '')
            location = data.get('location', '')
            highlights = data.get('highlights', [])
            tags = data.get('tags', [])
            
            # Format the job entry
            entry = f"\\cvevent{{\\textbf{{{self.escape_latex(title)}}}}}{{{self.escape_latex(company)}}}{{{self.escape_latex(dates)}}}{{{self.escape_latex(location)}}}\n"
            
            if highlights:
                entry += "\\begin{itemize}\n"
                for highlight in highlights:
                    # Convert markdown-style bold to LaTeX
                    highlight = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', highlight)
                    entry += f"  \\item {self.escape_latex(highlight)}\n"
                entry += "\\end{itemize}\n"
            
            if tags:
                tag_entries = []
                for tag in tags:
                    tag_entries.append(f"\\cvtag{{{self.escape_latex(tag)}}}")
                entry += ''.join(tag_entries) + '\n'
            
            sections.append(entry)
            
            # Add spacing between entries, but not after the last one
            if i < len(self.experiences) - 1:
                # Adjust spacing based on content length
                if len(highlights) > 3 or len(tags) > 5:
                    sections.append(r'\vspace{4pt}')
                else:
                    sections.append(r'\vspace{2pt}')
        
        return '\n'.join(sections)
    
    def format_diplomas_section(self) -> str:
        """Format diplomas section"""
        if not self.diplomas:
            return ""
        
        entries = []
        for title, data in self.diplomas.items():
            school = data.get('school', '')
            years = data.get('years', '')
            location = data.get('location', '')
            
            entry = f"\\cvevent{{\\faMortarBoard \\textbf{{{self.escape_latex(title)}}}}}{{{self.escape_latex(school)}}}{{{self.escape_latex(years)}}}{{{self.escape_latex(location)}}}"
            entries.append(entry)
        
        return '\n'.join(entries)
    
    def format_hard_skills_section(self) -> str:
        """Format hard skills section with ultra-compact spacing"""
        if not self.hard_skills:
            return ""
        
        sections = []
        for i, (category, skills) in enumerate(self.hard_skills.items()):
            if isinstance(skills, list):
                # Join skills with proper LaTeX separator
                skills_text = ' \\textbar{} '.join(skills)
                section = f"\\textcolor{{SlateGrey}}{{\\textbf{{{self.escape_latex(category)}}}}}\\\\\n{self.escape_latex(skills_text)}"
                sections.append(section)
                # Add very minimal spacing between categories, but not after the last one
                if i < len(self.hard_skills) - 1:
                    sections.append(r'\vspace{0.5pt}')
        
        return '\n\n'.join(sections)
    
    def format_soft_skills_section(self) -> str:
        """Format soft skills section with optimized spacing"""
        if not self.soft_skills:
            return ""
        
        sections = []
        for i, (category, skills) in enumerate(self.soft_skills.items()):
            if isinstance(skills, list):
                # Join skills with proper LaTeX separator
                skills_text = ' \\textbar{} '.join(skills)
                section = f"\\textcolor{{SlateGrey}}{{\\textbf{{{self.escape_latex(category)}}}}}\\\\\n{self.escape_latex(skills_text)}"
                sections.append(section)
                # Add minimal spacing between categories, but not after the last one
                if i < len(self.soft_skills) - 1:
                    sections.append(r'\vspace{1pt}')
        
        return '\n\n'.join(sections)
    
    def format_skills_section(self) -> str:
        """Format skills section with optimized spacing"""
        sections = []
        
        # Add hard skills
        if self.hard_skills:
            sections.append(r'\textcolor{SlateGrey}{\textbf{Hard Skills}}')
            for i, (category, skills) in enumerate(self.hard_skills.items()):
                if isinstance(skills, list):
                    # Join skills with proper LaTeX separator
                    skills_text = ' \\textbar{} '.join(skills)
                    section = f"\\textcolor{{SlateGrey}}{{\\textbf{{{self.escape_latex(category)}}}}}\\\\\n{self.escape_latex(skills_text)}"
                    sections.append(section)
                    # Add minimal spacing between categories, but not after the last one
                    if i < len(self.hard_skills) - 1:
                        sections.append(r'\vspace{1pt}')
        
        # Add soft skills
        if self.soft_skills:
            if sections:  # Add minimal spacing if hard skills were added
                sections.append(r'\vspace{3pt}')
            sections.append(r'\textcolor{SlateGrey}{\textbf{Soft Skills}}')
            for i, (category, skills) in enumerate(self.soft_skills.items()):
                if isinstance(skills, list):
                    # Join skills with proper LaTeX separator
                    skills_text = ' \\textbar{} '.join(skills)
                    section = f"\\textcolor{{SlateGrey}}{{\\textbf{{{self.escape_latex(category)}}}}}\\\\\n{self.escape_latex(skills_text)}"
                    sections.append(section)
                    # Add minimal spacing between categories, but not after the last one
                    if i < len(self.soft_skills) - 1:
                        sections.append(r'\vspace{1pt}')
        
        return '\n\n'.join(sections)
    
    def format_languages_section(self) -> str:
        """Format languages section"""
        if not self.languages:
            return ""
        
        entries = []
        for language, data in self.languages.items():
            level = data.get('level', '')
            descriptor = data.get('descriptor', '')
            entry = f"  \\item \\textbf{{{self.escape_latex(language)}}} \\hfill {self.escape_latex(level)} {self.escape_latex(descriptor)}"
            entries.append(entry)
        
        return '\n'.join(entries)
    
    def format_interests_section(self) -> str:
        """Format interests section like skills with categories"""
        if not self.interests:
            return ""
        
        sections = []
        for i, (category, interests_list) in enumerate(self.interests.items()):
            if isinstance(interests_list, list):
                # Join interests with proper LaTeX separator
                interests_text = ' \\textbar{} '.join(interests_list)
                section = f"\\textcolor{{SlateGrey}}{{\\textbf{{{self.escape_latex(category)}}}}}\\\\\n{self.escape_latex(interests_text)}"
                sections.append(section)
                # Add minimal spacing between categories, but not after the last one
                if i < len(self.interests) - 1:
                    sections.append(r'\vspace{1pt}')
        
        return '\n\n'.join(sections)
    
    def format_side_projects_section(self) -> str:
        """Format side projects section with optimized spacing and URLs in description"""
        if not self.side_projects:
            return ""
        
        sections = []
        for i, (project_id, data) in enumerate(self.side_projects.items()):
            title = data.get('title', project_id)
            role = data.get('role', 'Solo developer')
            dates = data.get('dates', '')
            location = data.get('location', '')
            highlights = data.get('highlights', [])
            tags = data.get('tags', [])
            url = data.get('url', '')
            
            # Format the project entry without "Side Project" in role
            entry = f"\\cvevent{{\\textbf{{{self.escape_latex(title)}}}}}{{{self.escape_latex(role)}}}{{{self.escape_latex(dates)}}}{{{self.escape_latex(location)}}}\n"
            
            if highlights:
                entry += "\\begin{itemize}\n"
                for highlight in highlights:
                    # Convert markdown-style bold to LaTeX
                    highlight = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', highlight)
                    entry += f"  \\item {self.escape_latex(highlight)}\n"
                
                # Add URL to the description if available
                if url and url != "Not public yet":
                    # Handle multiple URLs (comma-separated)
                    if ',' in url:
                        urls = [u.strip() for u in url.split(',')]
                        for url_item in urls:
                            # Escape underscores in display text for LaTeX
                            display_url = url_item.replace('_', r'\_')
                            entry += f"  \\item \\href{{{url_item}}}{{\\faExternalLink\\ {display_url}}}\n"
                    else:
                        # Escape underscores in display text for LaTeX
                        display_url = url.replace('_', r'\_')
                        entry += f"  \\item \\href{{{url}}}{{\\faExternalLink\\ {display_url}}}\n"
                
                entry += "\\end{itemize}\n"
            
            if tags:
                tag_entries = []
                for tag in tags:
                    tag_entries.append(f"\\cvtag{{{self.escape_latex(tag)}}}")
                entry += ''.join(tag_entries) + '\n'
            
            sections.append(entry)
            
            # Add spacing between entries, but not after the last one
            if i < len(self.side_projects) - 1:
                # Adjust spacing based on content length
                if len(highlights) > 2 or len(tags) > 4:
                    sections.append(r'\vspace{6pt}')
                else:
                    sections.append(r'\vspace{4pt}')
        
        return '\n'.join(sections)
    
    def generate_custom_tex(self):
        """Generate complete standalone LaTeX CV file"""
        print("Writing custom LaTeX file to", self.output_file)
        
        # Build the complete LaTeX document
        latex_content = self.build_complete_document()
        
        # Write to file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"Successfully generated {self.output_file}!")
    
    def build_complete_document(self) -> str:
        """Build complete standalone LaTeX document"""
        parts = []
        
        # Document header and packages
        parts.append(r'%%%%%%%%%%%%%%%%%')
        parts.append(r'% Updated CV tailored for Founding CTO role at JobTalk.ai')
        parts.append(r'%%%%%%%%%%%%%%%%%')
        parts.append(r'')
        parts.append(r'\documentclass[9pt,a4paper,ragged2e]{altacv}')
        parts.append(r'\usepackage[T1]{fontenc}')
        parts.append(r'\usepackage[utf8]{inputenc}')
        parts.append(r'\usepackage{paracol}')
        parts.append(r'\usepackage{hyperref}')
        parts.append(r'\usepackage{fontawesome}')
        parts.append(r'')
        parts.append(r'% Page geometry')
        parts.append(r'\geometry{%')
        parts.append(r'  left=1.5cm,')
        parts.append(r'  right=1.5cm,')
        parts.append(r'  top=1.5cm,')
        parts.append(r'  bottom=1.5cm,')
        parts.append(r'  marginparwidth=0pt,')
        parts.append(r'  marginparsep=0pt')
        parts.append(r'}')
        parts.append(r'')
        parts.append(r'% Fonts')
        parts.append(r'\ifxetexorluatex')
        parts.append(r'  \setmainfont{Carlito}')
        parts.append(r'\else')
        parts.append(r'  \usepackage[utf8]{inputenc}')
        parts.append(r'  \usepackage[T1]{fontenc}')
        parts.append(r'  \usepackage[default]{lato}')
        parts.append(r'\fi')
        parts.append(r'')
        parts.append(r'% Colours')
        parts.append(r'\definecolor{VividPurple}{HTML}{1282a2}')
        parts.append(r'\definecolor{VividPurplee}{HTML}{006c67}')
        parts.append(r'\definecolor{SlateGrey}{HTML}{001f54}')
        parts.append(r'\definecolor{LightGrey}{HTML}{0a1128}')
        parts.append(r'\colorlet{heading}{VividPurple}')
        parts.append(r'\colorlet{accent}{VividPurplee}')
        parts.append(r'\colorlet{emphasis}{SlateGrey}')
        parts.append(r'\colorlet{body}{LightGrey}')
        parts.append(r'')
        parts.append(r'% Bullet styles')
        parts.append(r'\renewcommand{\itemmarker}{{\small\textbullet}}')
        parts.append(r'\renewcommand{\ratingmarker}{\faCircle}')
        parts.append(r'')
        parts.append(r'\addbibresource{sample.bib}')
        parts.append(r'')
        parts.append(r'% ----------------------------------------------------------------------')
        parts.append(r'%                               HEADER')
        parts.append(r'% ----------------------------------------------------------------------')
        parts.append(r'\begin{document}')
        
        # Add personal info
        if self.profile:
            name = self.profile.get('name', '')
            tagline = self.profile.get('tagline', '')
            parts.append(f'\\name{{{self.escape_latex(name)}}}')
            parts.append(f'\\tagline{{{self.escape_latex(tagline)}}}')
            parts.append('')
            parts.append('\\personalinfo{')
            
            # Add contact information
            contact_info = self.format_contact_info()
            if contact_info:
                parts.append(contact_info)
            
            parts.append('}')
            parts.append('')
        
        parts.append(r'\begin{fullwidth}')
        parts.append(r'\makecvheader')
        parts.append(r'\end{fullwidth}')
        parts.append('')
        parts.append(r'% Ensure smaller font for itemize')
        parts.append(r'\AtBeginEnvironment{itemize}{\small}')
        parts.append('')
        
        # Add profile section
        if self.profile and self.profile.get('summary'):
            parts.append(r'% ----------------------------------------------------------------------')
            parts.append(r'%                               PROFILE')
            parts.append(r'% ----------------------------------------------------------------------')
            parts.append(r'\cvsection[]{Profil}')
            parts.append(f'{self.escape_latex(self.profile["summary"])}')
            parts.append('')
            parts.append(r'\vspace{4pt}')
            parts.append('')
        
        # Add main content layout
        main_layout = self.build_new_layout()
        parts.append(main_layout)
        
        # Close document
        parts.append(r'\end{document}')
        
        return '\n'.join(parts)
    
    def build_new_layout(self):
        """Build the new two-column layout"""
        layout_parts = []
        
        # First two-column section: Professional Experience and Diplomas
        layout_parts.append(r'% ----------------------------------------------------------------------')
        layout_parts.append(r'%                       PROFESSIONAL EXPERIENCE & DIPLOMAS')
        layout_parts.append(r'% ----------------------------------------------------------------------')
        layout_parts.append(r'\begin{paracol}{2}')
        layout_parts.append(r'% ----------------------------------------------------------------------')
        layout_parts.append(r'%                             COLUMN 1')
        layout_parts.append(r'% ----------------------------------------------------------------------')
        layout_parts.append(r'\cvsection{Professional experience}')
        
        # Add professional experience
        experience_section = self.format_experience_section()
        if experience_section:
            layout_parts.append(experience_section)
        else:
            layout_parts.append(r'\vspace{4pt}')
        
        # Add interests under professional experience in first column
        if self.interests:
            layout_parts.append(r'\vspace{4pt}')
            layout_parts.append(r'\cvsection{Interests}')
            interests_section = self.format_interests_section()
            if interests_section:
                layout_parts.append(interests_section)
        
        layout_parts.append(r'% ----------------------------------------------------------------------')
        layout_parts.append(r'%                             COLUMN 2')
        layout_parts.append(r'% ----------------------------------------------------------------------')
        layout_parts.append(r'\switchcolumn')
        layout_parts.append(r'\cvsection{Diplomas}')
        
        # Add diplomas
        diplomas_section = self.format_diplomas_section()
        if diplomas_section:
            layout_parts.append(diplomas_section)
        
        # Add hard skills under diplomas
        if self.hard_skills:
            layout_parts.append(r'\vspace{2pt}')
            layout_parts.append(r'\cvsection{Hard Skills}')
            hard_skills_section = self.format_hard_skills_section()
            if hard_skills_section:
                layout_parts.append(hard_skills_section)
        
        layout_parts.append(r'\end{paracol}')
        
        # Page break between sections
        layout_parts.append(r'\newpage')
        
        # Second two-column section: Side Projects and Soft Skills
        layout_parts.append(r'% ----------------------------------------------------------------------')
        layout_parts.append(r'%                         SIDE PROJECTS & SOFT SKILLS')
        layout_parts.append(r'% ----------------------------------------------------------------------')
        layout_parts.append(r'\begin{paracol}{2}')
        layout_parts.append(r'% ----------------------------------------------------------------------')
        layout_parts.append(r'%                             COLUMN 1')
        layout_parts.append(r'% ----------------------------------------------------------------------')
        layout_parts.append(r'\cvsection{Side projects}')
        
        # Add side projects
        side_projects_section = self.format_side_projects_section()
        if side_projects_section:
            layout_parts.append(side_projects_section)
        
        layout_parts.append(r'% ----------------------------------------------------------------------')
        layout_parts.append(r'%                             COLUMN 2')
        layout_parts.append(r'% ----------------------------------------------------------------------')
        layout_parts.append(r'\switchcolumn')
        
        # Add soft skills
        if self.soft_skills:
            layout_parts.append(r'\cvsection{Soft Skills}')
            soft_skills_section = self.format_soft_skills_section()
            if soft_skills_section:
                layout_parts.append(soft_skills_section)
        
        # Add languages under soft skills in second column
        if self.languages:
            layout_parts.append(r'')  # Add empty line for proper separation
            layout_parts.append(r'\vspace{2pt}')
            layout_parts.append(r'% ----------------------------------------------------------------------')
            layout_parts.append(r'%                             LANGUAGES')
            layout_parts.append(r'% ----------------------------------------------------------------------')
            layout_parts.append(r'\cvsection{Languages}')
            languages_section = self.format_languages_section()
            if languages_section:
                layout_parts.append(r'\begin{itemize}')
                layout_parts.append(languages_section)
                layout_parts.append(r'\end{itemize}')
        
        layout_parts.append(r'\end{paracol}')
        
        return '\n'.join(layout_parts)
    
    def run(self):
        """Main execution method"""
        print("Starting CV parsing process...")
        self.load_all_data()
        self.generate_custom_tex()
        print("CV parsing completed!")


def main():
    """Main function"""
    parser = SimpleCVParser()
    parser.run()


if __name__ == "__main__":
    main() 