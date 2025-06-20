import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel
from arxiv_helpers import get_arxiv_papers, get_first_page_pdf

load_dotenv()

DATE = datetime.now().strftime("%Y-%m-%d") # Must be of format YYYY-MM-DD

class Affiliations(BaseModel):
    affiliations: list[str]

if __name__ == "__main__":
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    print("Starting extraction...")
    # Try to get papers for DATE; if none, go back one day at a time until found
    check_date = datetime.now()
    while True:
        date_str = check_date.strftime("%Y-%m-%d")
        papers = get_arxiv_papers(date_str)
        if papers:
            DATE = date_str  # Update DATE to the found date
            print(f"Found papers for {DATE}")
            break
        check_date -= timedelta(days=1)
    print(f"Found {len(papers)} papers")
    for i, paper in enumerate(papers):
        if i % 10 == 0:
            print(f"Processing paper {i+1} of {len(papers)}")
        if i == len(papers) - 1:
            print(f"Processing paper {i+1} of {len(papers)}")
        first_page = get_first_page_pdf(paper["id"])
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite-preview-06-17",
            contents=f"Extract me the unique affiliations of the authors of the paper which first page is {first_page}",
            config={
                "response_mime_type": "application/json",
                "response_schema": Affiliations,
            },
        )
        papers[i]["affiliations"] = response.parsed.affiliations
    print(f"Extracted affiliations for {len(papers)} papers")
    with open("papers.json", "w") as f:
        json.dump(papers, f)
    print("Extraction complete and saved to papers.json")