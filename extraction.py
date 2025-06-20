import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel
from arxiv_helpers import get_arxiv_papers, get_first_page_pdf

load_dotenv()

DATE = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d") # Must be of format YYYY-MM-DD

class Affiliations(BaseModel):
    affiliations: list[str]

if __name__ == "__main__":
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    papers = get_arxiv_papers(DATE)
    for i, paper in enumerate(papers):
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
    with open("papers.json", "w") as f:
        json.dump(papers, f)