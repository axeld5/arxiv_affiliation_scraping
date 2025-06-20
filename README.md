# ArXiv Affiliation Scraper

A Python tool that extracts author affiliations from recent computer science papers on arXiv using AI-powered text analysis.

## Features

- Fetches papers from all CS categories published in the last 3 days
- Downloads and parses the first page of each paper's PDF
- Uses Google's Gemini AI to extract unique author affiliations
- Outputs results to `papers.json`

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your Gemini API key:
```bash
export GEMINI_API_KEY=your_api_key_here
```

3. Run the scraper:
```bash
python extraction.py
```

## Docker

```bash
docker build -t arxiv-scraper .
docker run --name arxiv-scraper-run arxiv-scraper
docker cp arxiv-scraper-run:/app/papers.json .
```

## Output

The script generates `papers.json` containing paper metadata and extracted affiliations for each author.
