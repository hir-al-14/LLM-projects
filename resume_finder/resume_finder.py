# Takes in the resume pdfs and seperates its sections using regular expression and makes a csv where each row consists of the data of a particular resume.
import requests
from bs4 import BeautifulSoup
import os

import pdfplumber
from pathlib import Path
import pandas as pd
import re
import string

def extract_text(pdf_path: Path) -> str:
    with pdfplumber.open(pdf_path) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]
    return "\n".join(pages)

SECTION_PATTERNS = {
    "education": re.compile(r"^education\b|academic\b|qualifications\b", re.I),
    "experience": re.compile(r"^(work\s+)?experience\b|employment\b", re.I),
    "skills": re.compile(r"^skills?\b|technical\s+skills\b", re.I),
    "projects": re.compile(r"^projects\b|technical\s+projects\b", re.I),
}

def split_sections(curr_text: str) -> dict:
    lines = [line.strip() for line in curr_text.splitlines() if line.strip()]
    sections = {"header": []}
    current_key = "header"

    for line in lines:
        matched = False
        for key, pattern in SECTION_PATTERNS.items():
            if pattern.match(line):
                current_key = key
                matched = True
                break
        if not matched:
            sections.setdefault(current_key, []).append(line)
    for key in sections:
        sections[key] = "\n".join(sections[key])
    return sections

def guess_name(header_text: str) -> str | None:
    for ln in header_text.splitlines():
        clean = ln.strip().translate(str.maketrans("", "", string.punctuation + "•|"))
        words = clean.split()
        if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w):
            return " ".join(words)
    return None

def parse_skills(skills_text: str) -> list[str]:
    tokens = re.split(r"[,;\n]", skills_text)
    skills = []

    for token in tokens:
        t = token.strip()

        if not t:
            continue

        if "@" in t and "." in t:
            continue

        digits = re.sub(r"\D", "", t)
        if len(digits) >= 10:
            continue

        skills.append(t.title())

    return sorted(set(skills))

def resume_to_row(sections: dict[str, str]) -> dict:
    return {
        "name": guess_name(sections.get("header", "")),
        "education": sections.get("education", ""),
        "experience": sections.get("experience", ""),
        "skills": "; ".join(parse_skills(sections.get("skills", ""))),
        "projects": sections.get("projects", ""),
    }

def main():
    rows = []
    for pdf_file in Path("resumes").glob("*.pdf"):
        extracted_text = extract_text(pdf_file)
        sections = split_sections(extracted_text)
        
        row = resume_to_row(sections)

        row["source_file"] = pdf_file.name

        rows.append(row)
    
    df = pd.DataFrame(rows)
    Path("output").mkdir(exist_ok=True)
    df.to_csv("output/resume_index.csv", index=False)
    print(f"Wrote {len(rows)} rows to output/resume_index.csv") 
 
if __name__ == "__main__":
    main()


'''
def download_resumes():
    base_url = "https://www.northguru.com/media/cv/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    os.makedirs("resumes", exist_ok=True)

    pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]

    for i, link in enumerate(pdf_links[:20]):
        full_url = link if link.startswith("https") else base_url + linka
        print(f"Downloading: {full_url}")

        try:
            pdf_data = requests.get(full_url)
            with open(f"resumes/resume_{i}.pdf", 'wb') as f:
                f.write(pdf_data.content)
        except Exception as e:
            print(f"Could not download {full_url}: {e}")
'''