import argparse
import requests
from lxml import html

# Command-Line Argument Parsing
parser = argparse.ArgumentParser(description='Compare headings between two technical documents.')
parser.add_argument('url1', type=str, help='URL of the first document')
parser.add_argument('url2', type=str, help='URL of the second document')
args = parser.parse_args()

# Fetch Document
def fetch_document(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise ValueError(f"Failed to fetch document from {url}")

# Parse Headings
def parse_headings(html_content):
    tree = html.fromstring(html_content)
    headings = []
    for i in range(1, 7):
        xpath_expr = f"//h{i}"
        elements = tree.xpath(xpath_expr)
        for elem in elements:
            text = elem.text_content().strip()
            if text:  # Ensure that empty headings are not included
                headings.append((i, text))
    return headings

# Find Missing Headings
def find_missing_headings(headings1, headings2):
    headings1_dict = {text: level for level, text in headings1}
    headings2_dict = {text: level for level, text in headings2}
    
    missing_in_2 = [(level, text) for text, level in headings1_dict.items() if text not in headings2_dict]
    missing_in_1 = [(level, text) for text, level in headings2_dict.items() if text not in headings1_dict]
    
    return missing_in_2, missing_in_1

# Report Missing Headings
def report_missing_headings(missing_in_2, missing_in_1):
    missing_in_2.sort()  # Sort by level and then text
    missing_in_1.sort()  # Sort by level and then text
    
    if missing_in_2:
        print("Headings in Document 1 missing in Document 2:")
        for level, text in missing_in_2:
            print(f"  - {'#' * level} {text}")
    else:
        print("No headings from Document 1 are missing in Document 2.")
    
    if missing_in_1:
        print("Headings in Document 2 missing in Document 1:")
        for level, text in missing_in_1:
            print(f"  - {'#' * level} {text}")
    else:
        print("No headings from Document 2 are missing in Document 1.")

# Main Function
if __name__ == "__main__":
    url1, url2 = args.url1, args.url2

    # Fetch and parse documents
    doc1 = fetch_document(url1)
    doc2 = fetch_document(url2)
    headings1 = parse_headings(doc1)
    headings2 = parse_headings(doc2)

    # Find missing headings
    missing_in_2, missing_in_1 = find_missing_headings(headings1, headings2)

    # Report missing headings
    report_missing_headings(missing_in_2, missing_in_1)
