


# Search Engine
### Introduction
This is a Java and Python-based search engine that retrieves web pages from a given set of URLs and enables users to perform keyword-based search on these pages.

### Approach
The search engine is built using the following steps:

Web Crawling: The content of each URL is retrieved using the crawl_url() function from the WebCrawler.py file.
Tokenization: The content of each page is split into individual words using the tokenize() function.
Inverted Index: An inverted index is built for all the words across all pages. The inverted index is a data structure that maps each word to a list of pages that contain that word, along with the frequency of that word in each page.
Ranking: A ranking algorithm is used to score each page based on the relevance of the query to the content of that page. The ranking algorithm used in this search engine is BM25, which is a popular ranking function used in information retrieval. The algorithm calculates a score for each page based on the frequency of query terms in that page and the importance of those terms in the overall corpus of pages.
Search: The user's query is tokenized and used to search the inverted index for pages that contain those terms. The ranking algorithm is then applied to these pages to sort them in order of relevance to the query.
### Algorithms and Data Structures
The following algorithms and data structures are used in this search engine:

Tokenization: This algorithm splits the text of each page into individual words and removes stop words and non-alphabetic words with digits.
Inverted Index: This data structure maps each word to a list of pages that contain that word, along with the frequency of that word in each page.
BM25 Ranking Algorithm: This algorithm calculates a score for each page based on the frequency of query terms in that page and the importance of those terms in the overall corpus of pages.
### How to Use
To use this search engine, follow these steps:

Create a text file named input_urls.txt in the same directory as the search_engine_finalupdated.py file. Add the URLs of the pages you want to include in the search engine, one URL per line.
Run the search_engine_finalupdated.py file. This will build the inverted index for the pages and prompt you to enter a query.
Enter a query and the number of results you want to see. The search engine will return the top results based on the relevance of the query to the content of the pages.
crawler that can automatically discover new pages to add to the search engine.
