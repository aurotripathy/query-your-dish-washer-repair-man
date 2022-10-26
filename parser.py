# bs4 hacking ideas from https://stackoverflow.com/questions/34589064/beautifulsoup-get-the-class-text

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import csv
import re
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer

def gen_text_for_embeddings(url, f, writer, total, title):
    """total is the sentence count up to this point"""
    
    html_text = requests.get(url).text
    
    soup = BeautifulSoup(html_text, 'html.parser')
    merge_text = None
    for i, para in enumerate(soup.findAll('p')):
        # writer.writerow([f'***{i}***'])
        text = ''
        if para.find_all('strong'):
            merge_text = para.text
            continue
        if merge_text is not None:
            text = '' + merge_text + ' '
            merge_text = None
    
        for child in para:
            
            if isinstance(child, NavigableString):
                text += str(child).strip()
                text = re.sub(r"(\231|\200|\204)", "", text)  # cleanup
            elif isinstance(child, Tag):
                if child.name != 'br' or child.name != 'em':
                    text = text + ' ' + child.text + ' '
                else:
                    text += '\n'
        
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(text)
        heading = TreebankWordDetokenizer().detokenize(tokens[:5])
        # writer.writerow([title, heading, text, len(tokens)])
        writer.writerow([title, f'{str(total + i)}', text, len(tokens)])
    return total + len(soup.find_all('p')) 

# main
out_file = 'dish-washer-data.csv'   
f_handle = open(out_file, 'w')
writer = csv.writer(f_handle, quoting=csv.QUOTE_ALL)
writer.writerow(["title", "heading", "content", "tokens"])
total_sentences = 0
for i in range(1, 7):
    title = f'Chapter_{i}'
    url = f'https://www.appliancerepair.net/dishwasher-repair-{i}.html'
    total_sentences = gen_text_for_embeddings(url, f_handle, writer, total_sentences, title)   
f_handle.close()