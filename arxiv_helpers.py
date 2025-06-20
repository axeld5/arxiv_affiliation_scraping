import io
import fitz  # PyMuPDF
import requests
import xml.etree.ElementTree as ET

CS_CLASSES = [
    'cs.' + cat for cat in [
        'AI', 'AR', 'CC', 'CE', 'CG', 'CL', 'CR', 'CV', 'CY', 'DB',
        'DC', 'DL', 'DM', 'DS', 'ET', 'FL', 'GL', 'GR', 'GT', 'HC',
        'IR', 'IT', 'LG', 'LO', 'MA', 'MM', 'MS', 'NA', 'NE', 'NI',
        'OH', 'OS', 'PF', 'PL', 'RO', 'SC', 'SD', 'SE', 'SI', 'SY',
    ]
]

def get_arxiv_papers(date):
    papers = []    
    title_list = []
    for cls in CS_CLASSES:
        query = f"http://export.arxiv.org/api/query?search_query=cat:'{cls}'&sortBy=submittedDate&sortOrder=descending"
        params = {
                "start": 0,
                "max_results": 100
        }
        response = requests.get(query, params=params)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            entries = root.findall('{http://www.w3.org/2005/Atom}entry')
            for entry in entries:
                paper = {
                    'id': entry.find('{http://www.w3.org/2005/Atom}id').text,
                    'title': entry.find('{http://www.w3.org/2005/Atom}title').text,
                    'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text,
                    'authors': [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')],
                    'published': entry.find('{http://www.w3.org/2005/Atom}published').text
                }
                paper["author_count"] = len(paper["authors"])
                if date in paper["published"]:
                    if paper["title"] not in title_list:
                        papers.append(paper)
                        title_list.append(paper["title"])
    return papers


def get_first_page_pdf(arxiv_id):
    """
    Given an arXiv paper id (e.g., 'http://arxiv.org/abs/2406.12345'), 
    download the PDF and extract the first page as text.
    Returns the first page text, or None if failed.
    """
    # Extract the arxiv number from the id
    if arxiv_id.startswith("http"):
        arxiv_num = arxiv_id.split('/')[-1]
    else:
        arxiv_num = arxiv_id
    pdf_url = f"https://arxiv.org/pdf/{arxiv_num}.pdf"
    try:
        resp = requests.get(pdf_url)
        if resp.status_code == 200:
            pdf_bytes = io.BytesIO(resp.content)
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            if doc.page_count > 0:
                first_page = doc.load_page(0)
                text = first_page.get_text()
                return text
        else:
            print(f"Failed to download PDF: {pdf_url}")
    except Exception as e:
        print(f"Error extracting first page: {e}")
    return None