
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

from modules.tool import ToolsFactory

from duckduckgo_search import DDGS

import concurrent.futures

from bs4 import BeautifulSoup

from unstructured.partition.html import partition_html

exluded = ["youtube.com"]
search_limit = 5

### TOOL FUNCTION

def web_search(args):
    """Fetches the content of a web search for a given search_query"""

    print(f"[TOOL][web_search] search_query: {args["search_query"]}")
    links = duckduckgo_search(args["search_query"], limit=search_limit)

    contents = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(read_web_page, url["href"]) for url in links]
        for future in concurrent.futures.as_completed(futures):
            content = future.result()
            if content:
                contents.append(content)

    return contents

### LLM TOOL DEFINITION

tool_factory = ToolsFactory()
search_query_parameter = tool_factory.new_tool_parameter(name="search_query", description="Search query for finding the contents on the search engine", required=True)
tool_parameters = [search_query_parameter]

tool_description = (
        "Search the web and fetch the content of the most relevant pages."
        "Always use this if you dont know something or the user is asking for something that is likely found online."
        "Augment the search query with all the information needed to find content online."
)
web_search_tool = tool_factory.new_tool(function=web_search, description=tool_description, parameters=tool_parameters)

### UTILITY FUNCTION

def duckduckgo_search(query, site = None, limit = 1, lang="en"):
    if site:
        query += f" site:{site}"
    for site in exluded:
        query += f" -{site}"
    results = DDGS().text(query, max_results=limit)
    # results = search(query, num_results=limit, lang=lang, region=lang  ,unique=True)
    return results

def read_web_page(link):
    
    print(f"[UTIL][read_web_page] link: {link}")
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    result = requests.get(link, headers=headers, verify=False)
    if result.status_code != 200:
        print(f"! status code: {result.status_code}")
        return None
    
    soup = BeautifulSoup(result.text, features="html.parser")

    for script in soup.body.select('script'):
        script.decompose()

    for img in soup.body.select('img'):
        img.decompose()

    for span in soup.body.select('span'):
        span.decompose()

    for tags in soup.body.find_all(): 
        for val in list(tags.attrs):
            del tags.attrs[val]

    elements = partition_html(text=soup.body.prettify(), chunking_strategy="by_title")

    page_content = ""
    for element in elements:
        page_content += element.text

    return {"content":page_content, "source":link}

if __name__ == "__main__":

    x = duckduckgo_search("ciao", limit=5)
    print(x)