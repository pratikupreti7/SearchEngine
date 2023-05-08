import re
import sys

import requests
import string
from collections import Counter
import math

# Import the crawl_url function from webcrawler.py
from WebCrawler import crawl_url

def search_engine():
    # Define stop words
    stop_words = {"a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he", "in", "is", "it", "its",
                  "of", "on", "that", "the", "to", "was", "were", "will", "with"}

    def tokenize(text):
        # Remove punctuation and convert to lowercase
        text = text.translate(str.maketrans("", "", string.punctuation)).lower()
        # Split into words
        words = text.split()
        # Remove stop words and non-alphabetic words with digits
        words = [word for word in words if
                 word not in stop_words and not re.match('\W+', word) and not any(char.isdigit() for char in word)]
        return words

    class TrieNode:
        def __init__(self):
            self.word_ids = []  # A list to store the IDs of the pages where the word appears
            self.word_freqs = []  # A list to store the frequency of the word in each page
            self.headings = []  # A list to store the headings where the word appears
            self.children = {}

    class Trie:
        def __init__(self):
            self.root = TrieNode()

        def insert(self, word, page_id, freq, heading):
            node = self.root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            if not node.word_ids or node.word_ids[-1] != page_id:
                node.word_ids.append(page_id)
                node.word_freqs.append(0)
                node.headings.append("")
            node.word_freqs[-1] += freq
            node.headings[-1] += " " + " ".join(heading)


        def get_node(self, word):
            node = self.root
            for char in word:
                if char in node.children:
                    node = node.children[char]
                else:
                    return None
            return node



    def build_inverted_index(pages, headings_list):
        inverted_index = {}
        for i, (page, headings) in enumerate(zip(pages, headings_list)):
            words = tokenize(page)
            word_freqs = Counter(words)
            for word, freq in word_freqs.items():
                if word not in inverted_index:
                    inverted_index[word] = {"freqs": [], "ids": [], "headings": []}
                inverted_index[word]["ids"].append(i)
                inverted_index[word]["freqs"].append(freq)
                inverted_index[word]["headings"].append(headings)
        inverted_index["__num_pages__"] = len(pages)
        return inverted_index


    def bm25(query_word, page_id, inverted_index, avg_doc_len, k1=1.2, b=0.75):
        node = inverted_index.get_node(query_word)
        if not node or page_id not in node.word_ids:
            return 0

        index = node.word_ids.index(page_id)
        term_freq = node.word_freqs[index]
        doc_len = sum(node.word_freqs)
        doc_count = inverted_index.page_count
        n = len(node.word_ids)

        idf = math.log((doc_count - n + 0.5) / (n + 0.5))
        numerator = term_freq * (k1 + 1)
        denominator = term_freq + k1 * (1 - b + b * (doc_len / avg_doc_len))

        return idf * (numerator / denominator)

    def search(query, urls, pages, inverted_index, num_results=None):
        query_words = tokenize(query)
        query_freqs = Counter(query_words)
        if not query_words or not inverted_index:
            return []

        result = set()
        for word in query_words:
            try:
                if word in inverted_index:
                    result.update(inverted_index[word]["ids"])
            except KeyError:
                continue

        search_results = []
        for page_id in result:
            if 0 <= page_id < len(urls) and 0 <= page_id < len(pages):
                score = 0
                query_counts = {}
                for word in query_words:
                    try:
                        if page_id in inverted_index[word]["ids"]:
                            index = inverted_index[word]["ids"].index(page_id)
                            freq = inverted_index[word]["freqs"][index]
                            if index >= 0 and index < len(inverted_index[word]["headings"]) and word in \
                                    inverted_index[word]["headings"][index]:
                                score += freq * query_freqs[word] * 2
                            else:
                                score += freq * query_freqs[word]
                            query_counts[word] = pages[page_id].lower().count(word.lower())
                        elif index >= 0 and index < len(inverted_index[word]["headings"]) and word in \
                                inverted_index[word]["headings"][index]:
                            if index >= 0 and index < len(inverted_index[word]["headings"]) and word in \
                                    inverted_index[word]["headings"][index]:
                                score += query_freqs[word] * 0.5
                    except KeyError:
                        continue
                if isinstance(page_id, int):
                    search_results.append(
                        (urls[page_id], ' '.join(pages[page_id].split()[:5]) + '...', score, query_counts))
        search_results = sorted(search_results, key=lambda x: x[2], reverse=True)

        if len(search_results) == 0:
            return []
        else:
            if num_results is not None:
                search_results = search_results[:num_results]
            return search_results

    pages = []
    headings_list = []
    # Read urls from input_urls.txt file
    with open('input_urls.txt', 'r') as file:
        urls = [line.strip() for line in file]
        for url in urls:
            try:
                content, headings = crawl_url(url)
                pages.append(content)
                headings_list.append(headings)
            except:
                print(f"Error: Could not retrieve page content for {url}")

    inverted_index = build_inverted_index(pages, headings_list)

    import sys

    import sys

    # Open the output file before the loop
    import sys


    while True:
        print("-----------------------------------------------------------------------------------")
        query = input("Enter a query or 'q' to quit: ")
        if query == 'q':
            break
        print("-----------------------------------------------------------------------------------")
        num_results_input = input("Enter the number of results you want to see or 't' for top results: ")
        try:
            if num_results_input == 't':
                num_results = 1
            else:
                num_results = int(num_results_input)

            # Perform search
            search_results = search(query, urls, pages, inverted_index, num_results)

            # Print results to console and file
            output_str = ""
            if len(search_results) == 0:
                output_str += "No results found. Please enter meaningful text, try avoiding stop words or just numbers."
            else:
                output_str += f"{len(search_results)} results found:\n"
                for i, result in enumerate(search_results):
                    page_id = urls.index(result[0])
                    query_counts = result[3]

                    output_str += f"\n-----------------------------------------------------------------------------------\n\n"
                    output_str += f"{i + 1}. {result[0]} - {result[1]} - Score: {result[2]}\n"
                    for word, count in query_counts.items():
                        output_str += f"'{word.title()}' appeared {count} times\n"
                    output_str += "\n"

            # Print to console
            print(output_str)

            # Save to file
            with open("output.txt", "a") as f:
                f.write(output_str)

        except ValueError:
            print("-----------------------------------------------------------------------------------")
            print(
                "Invalid input for the number of search results. Please enter a positive integer or 't' for top result.")
            print("-----------------------------------------------------------------------------------")


if __name__ == '__main__':
    search_engine()


