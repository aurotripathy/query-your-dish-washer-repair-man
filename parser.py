# bs4 hacking ideas from https://stackoverflow.com/questions/34589064/beautifulsoup-get-the-class-text

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import csv
import re
from nltk.tokenize import RegexpTokenizer

def gen_text_for_embeddings(url, f, total):
    """total is the sentence count up to this point"""
    writer = csv.writer(f)
    
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    #remove any 'funny' characters
    #import re module
    
    #re.sub() method
    # soup = re.sub(r"(\200|\232)", "", soup)


    # allowlist = ['p',]

    # f.write(f'*************Table-of-Contents*************\n')
    # for div in soup.findAll('div', {'class': 'toc-category'}):
    #     f.write(f'{str(div.find_all(text=True))}\n')

    soup = BeautifulSoup(html_text, 'html.parser')
    for i, para in enumerate(soup.findAll('p')):
        # writer.writerow([f'***{i}***'])
        text = ''
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
        writer.writerow([total + i, text, len(tokens)])
    return total + len(soup.find_all('p')) 

# main
out_file = 'out-file.csv'   
f_handle = open(out_file, 'w')
total_sentences = 0
for i in range(1, 6):
    url = f'https://www.appliancerepair.net/dishwasher-repair-{i}.html'
    total_sentences = gen_text_for_embeddings(url, f_handle, total_sentences)   
f_handle.close()