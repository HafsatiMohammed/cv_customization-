# CV Generator Project

This project automatically generates a professional CV in PDF format from structured JSON data using Python parsing and LaTeX compilation.

## 📁 Project Structure

```
CV/
├── README.md                           # This file
├── CV_json/                            # Source data files (JSON-like Python dictionaries)
│   ├── profile.json                    # Personal information, summary, objective
│   ├── Professional_experience.json    # Work experience entries
│   ├── diplomas.json                   # Educational background
│   ├── languages.json                  # Language proficiencies
│   ├── hard_skills.json               # Technical skills and competencies
│   ├── soft_skills.json               # Interpersonal and leadership skills
│   ├── Interest.json                   # Personal interests and hobbies
│   └── side_projects.json             # Personal projects with URLs
├── CV_python_parser/                   # Python parsing engine
│   ├── cv_parser_simple.py            # Main parser (generates complete LaTeX)
│   ├── run_parser.py                  # Simple runner script
│   ├── requirements.txt               # Dependencies (none - uses standard library)
│   └── README.md                      # Parser-specific documentation
└── CV_tex/                            # LaTeX output and templates
    ├── isso.tex                       # Original template (reference only)
    └── isso_custom.tex                # Generated LaTeX file (compiled to PDF)
```

## 🎯 Generated PDF Structure

The final CV is organized in a **two-page, two-column layout**:

### **Page 1: Professional Experience & Diplomas**
- **Column 1:**
  - Professional Experience (chronological order)
  - Languages (after experience)
  - Interests (after languages)
- **Column 2:**
  - Diplomas (educational background)
  - Hard Skills (technical competencies)

### **Page 2: Side Projects & Soft Skills**
- **Column 1:**
  - Side Projects (with clickable URLs)
- **Column 2:**
  - Soft Skills (leadership, communication, etc.)
  - Languages (repeated for balance)

## 🔄 Data Flow Process

### 1. **JSON Data Sources** (`CV_json/`)
Each JSON file contains structured data in Python dictionary format:

- **`profile.json`**: Personal info, contact details, summary, objective
- **`Professional_experience.json`**: Work history with roles, companies, dates, highlights, tags
- **`diplomas.json`**: Educational background with degrees, schools, years, locations
- **`languages.json`**: Language proficiencies with levels
- **`hard_skills.json`**: Technical skills organized by categories
- **`soft_skills.json`**: Interpersonal skills organized by categories
- **`Interest.json`**: Personal interests organized by categories
- **`side_projects.json`**: Personal projects with descriptions and GitHub URLs

### 2. **Python Parsing** (`CV_python_parser/`)
The `cv_parser_simple.py` script:

- **Loads** JSON-like Python dictionary files
- **Processes** and **escapes** content for LaTeX compatibility
- **Formats** each section with proper LaTeX commands
- **Generates** a complete, standalone LaTeX document
- **Outputs** `isso_custom.tex` in the `CV_tex/` folder

### 3. **LaTeX Generation** (`CV_tex/`)
The parser generates a complete LaTeX document including:

- **Document class** and **packages** (altacv, paracol, hyperref, fontawesome)
- **Page geometry** and **color definitions**
- **Header** with personal information
- **Two-column layout** using `paracol` environment
- **Section formatting** with `\cvsection`, `\cvevent`, `\cvtag`
- **Clickable URLs** for side projects using `\href{}`
- **Proper spacing** and **typography**

### 4. **PDF Compilation**
The final `isso_custom.tex` file is compiled to PDF using:
```bash
pdflatex isso_custom.tex
```

## 🚀 Usage Instructions

### Quick Start
1. **Navigate to the parser directory:**
   ```bash
   cd CV_python_parser
   ```

2. **Run the parser:**
   ```bash
   python cv_parser_simple.py
   ```

3. **Compile to PDF:**
   ```bash
   cd ../CV_tex
   pdflatex isso_custom.tex
   ```

### Customization

#### **Modifying Content**
- Edit the JSON files in `CV_json/` to update your information
- The parser will automatically handle LaTeX escaping and formatting

#### **Layout Adjustments**
- Modify the `build_new_layout()` method in `cv_parser_simple.py`
- Adjust spacing with `\vspace{}` commands
- Reorganize sections by changing the column assignments

#### **Styling Changes**
- Colors are defined in the `build_complete_document()` method
- Font and geometry settings are in the LaTeX preamble
- Section formatting is handled by individual `format_*_section()` methods

## 🔧 Technical Features

### **LaTeX Escaping**
The parser automatically handles:
- Special LaTeX characters (`&`, `%`, `$`, `#`, `_`, `^`, `\`, `~`, `{`, `}`)
- Unicode characters (en-dashes, em-dashes, arrows, multiplication symbols)
- Mathematical expressions (numbers with operators)
- Already-formatted LaTeX commands (prevents double-escaping)

### **URL Handling**
- Side project URLs are automatically converted to clickable LaTeX links
- FontAwesome icons (`\faExternalLink`) are added to links
- Underscores in display text are properly escaped

### **Spacing Optimization**
- Dynamic spacing based on content length
- Ultra-compact spacing for skills sections
- Proper line breaks between sections

### **Error Handling**
- Robust JSON-like file parsing with syntax error correction
- Graceful handling of missing data
- Comprehensive Unicode character conversion

## 📋 Requirements

### **System Requirements**
- Python 3.6+ (uses only standard library)
- LaTeX distribution (TeX Live, MiKTeX, etc.)
- `pdflatex` command available

### **LaTeX Packages**
The generated document uses:
- `altacv` (CV document class)
- `paracol` (two-column layout)
- `hyperref` (clickable links)
- `fontawesome` (icons)
- `geometry` (page layout)
- `color` (custom colors)

## 🎨 Design Features

### **Color Scheme**
- **Primary**: VividPurple (#1282a2)
- **Secondary**: VividPurplee (#034078)
- **Text**: SlateGrey (#001f54)
- **Body**: LightGrey (#0a1128)

### **Typography**
- **Main font**: Lato (default)
- **Icons**: FontAwesome
- **Section headers**: Bold with custom colors
- **Tags**: Colored badges for skills

### **Layout**
- **Two-column responsive design**
- **Compact spacing** for maximum content density
- **Professional typography** and spacing
- **Clickable elements** for digital viewing

## 🔄 Maintenance

### **Adding New Sections**
1. Create a new JSON file in `CV_json/`
2. Add a corresponding `format_*_section()` method in the parser
3. Include the section in `build_new_layout()`

### **Updating Templates**
- The parser generates complete LaTeX documents
- No external template dependencies
- All styling is self-contained

### **Version Control**
- JSON files contain the source data
- Python parser contains the logic
- Generated LaTeX can be regenerated anytime

## 📞 Support

For issues or questions:
1. Check the JSON file syntax
2. Verify LaTeX installation
3. Review the parser error messages
4. Ensure all required packages are installed

---

**Note**: This project generates professional CVs optimized for both print and digital viewing, with automatic LaTeX escaping, clickable links, and responsive two-column layout. 