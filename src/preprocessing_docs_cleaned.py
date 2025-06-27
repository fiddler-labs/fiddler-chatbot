# Follow these steps to reload the vector index, currently running in DataStax
"""
* **Gather Data** 
    * Clear out the old doc content folders if necessary
        * Delete old content source: documentation_data/vector_index_feed_v2x.x.csv
        * Clear out:
          * documentation_data/fiddler-docs
          * documentation_data/md-notebooks
          * documentation_data/notebooks-ipynb
    * Download The [docs](https://github.com/fiddler-labs/fiddler/tree/main/docs) folder from the [Fiddler Repo](https://github.com/fiddler-labs/fiddler/docs)
        * Clone or Make a pull request on the repo
        * Make sure this is pulled from the branch corresponding to the current release (branch name should be `release/2x.x`)
        * Copy the "docs" folder contents to fiddler-chatbot/documentation_data/fiddler-docs
    * Copy the latest [quickstart notebooks](https://github.com/fiddler-labs/fiddler-examples)
        * Make sure to grab the notebook from the latest release
        * Place all the .ipynb files from for the lastest release in fiddler-chatbot/documentation_data/notebooks-ipynb
* **Run this notebook to generate the vector index feed for this verison**
    * Update the `release_num` flag (in set state step) to the release version you are loading the docs for
    * Generate the markdown version of .ipynb files and add it to quickstart pages on with the script below
    * Crawl the our website for blog and other resources
    * You will need to add the caveats from last version the current version
    * Chunk the data
    * Finally we generate the vector_index_feed_2x.x.csv that we will upload to our vector database

* **Last step:** Reloading the vector index table is done via the "loader_cassandra_vector_index.ipynb" notebook. Open that notebook and follow the instructions there
"""

import os

import pandas as pd
import re
import feedparser
from bs4 import BeautifulSoup
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter

# EMBEDDING_MODEL = "text-embedding-3-large"  # OpenAI's latest and most capable embedding model
# GPT_MODEL = "gpt-4-turbo"
release_num = 'v25.10'
source_doc_path = './documentation_data'
fiddler_doc_path = f'{source_doc_path}/fiddler-docs'
quickstarts_doc_path = f'{fiddler_doc_path}/tutorials-and-quick-starts'
quickstart_notebooks_path = f'{source_doc_path}/notebooks-ipynb'
nbconverted_output_path = f'{source_doc_path}/md-notebooks'


# Append Notebook markdowns to quick starts
# Download the latest [Quickstart guides](https://github.com/fiddler-labs/fiddler-examples/tree/main/quickstart/latest) into *documentation_data/notebooks-ipynb* folder: 
# Running the NBConvert in the next step will update the md-notebooks folder with markdown version of all the quickstarts from the *notebooks-ipynb* directory 

!jupyter nbconvert --output-dir={nbconverted_output_path} {quickstart_notebooks_path}/* --to markdown

# the script dynamically injects the full text of quickstart notebook tutorials into their corresponding documentation pages, 
# ensuring the docs are comprehensive and self-contained.

for root, dirs, files in os.walk(quickstarts_doc_path): 
    for name in files:
        path = os.path.join(root, name)
        print(path)
        if path[-3:] == '.md':
            with open(path,'r') as f:
                file_str = f.read()
            ipynb_links = re.search(r'\bFiddler_Quickstart_\w+', file_str)
            print(ipynb_links)
            if ipynb_links:
                f = f'{nbconverted_output_path}/{ipynb_links.group()}.md'
                print(f)
                with open(f,'r') as l: 
                    QS = l.read()
                    # print(QS)
                with open(path, 'a') as f:
                    f.write(QS)
                    print(ipynb_links.group())


# The cell will take the markdown version of the notebooks and append it to the quickstart pages in the documentation directory 
# Creating list of chunked_docs from downloaded documentation 
# change the path to where your downloaded folder is and choose the version of the docs you want to process
source_docs = []
for root, dirs, files in os.walk(fiddler_doc_path):
    for name in files:
        path = os.path.join(root, name)
        if path[-3:] == ".md":
            with open(path, "r") as f:
                file_str = f.read()
                # Embed the URL of the doc in the file so the LLM doesn't have to look it up 
                doc_url = f'DOC_URL:{path[:-3]}'
                doc_content = f'DOC_CONTENT:{file_str}'
                source_docs.append(f'{doc_url}\n{doc_content}')
print(source_docs[0])
len(source_docs)

# Crawl the blog and resources content and append it to chunked_doc list

def crawl_rss_feed(rss_url):
    # Parse the RSS feed
    feed = feedparser.parse(rss_url)

    print("Number of Blogs:", len(feed.entries))
    
    # Iterate through the entries in the feed
    for entry in feed.entries:

        # Get the URL of the blog article
        article_url = entry.link

        # Fetch the content of the article
        response = requests.get(article_url)
        html_content = response.content.decode('utf-8', 'ignore')

        # Use BeautifulSoup to parse the HTML and extract the body
        soup = BeautifulSoup(html_content, 'html.parser')
        div_content = soup.find('div', class_='blog-post_content-wrapper')  # You may need to adjust this based on the HTML structure

        # Print or manipulate the content of the div
        if div_content:
            print("Title:", entry.title)
            print("Link:", entry.link)
            itemtext=''
            for item in div_content.select('p'):
                itemtext+=item.text + ' '
            source_docs.append(f"BlogLink:{entry.link}\nContent: {itemtext}")
        else:
            print("Div not found.")

# Replace 'your_rss_feed_url' with the actual RSS feed URL
rss_feed_url = 'https://www.fiddler.ai/blog/rss.xml'
crawl_rss_feed(rss_feed_url)

# Mostly duplicate code, consider refactoring

def crawl_rss_feed(rss_url):
    # Parse the RSS feed
    feed = feedparser.parse(rss_url)

    print("Number of Resources:", len(feed.entries))
    
    # Iterate through the entries in the feed
    for entry in feed.entries:

        # Get the URL of the blog article
        article_url = entry.link

        # Fetch the content of the article
        response = requests.get(article_url)
        html_content = response.content.decode('utf-8', 'ignore')

        # Use BeautifulSoup to parse the HTML and extract the body
        soup = BeautifulSoup(html_content, 'html.parser')

        
        div_content = soup.find('div', class_='resources-copy')  # You may need to adjust this based on the HTML structure

        # Print or manipulate the content of the div
        if div_content:
            print("Title:", entry.title)
            print("Link:", entry.link)
            itemtext=''
            for item in div_content.select('p'):
                itemtext+=item.text + ' '
            source_docs.append(f"ResourceLink:{entry.link}\nContent:{itemtext}")
        else:
            print("Div not found.")

# Replace 'your_rss_feed_url' with the actual RSS feed URL
rss_feed_url = 'http://www.fiddler.ai/resources/rss.xml'
crawl_rss_feed(rss_feed_url)

len(source_docs)



chunked_doc = [item.strip() for item in source_docs]
print(len(chunked_doc))
# text_splitter = TokenTextSplitter(chunk_size=400, chunk_overlap=40)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=300,
    length_function=len
)

chunked_doc_with_overlap = []

for doc in chunked_doc:
    texts = text_splitter.split_text(doc)
    chunked_doc_with_overlap = chunked_doc_with_overlap + texts

print(len(chunked_doc_with_overlap))

df = pd.DataFrame(chunked_doc_with_overlap, columns=['text'])
df.to_csv(f'documentation_data/vector_index_feed_{release_num}.csv', index=False)
df

# Please check the **vector_index_feed_{release_num}.csv** file and navigate to loader_casandra_vector_index.ipynb to upload these snippets to our vector database.


