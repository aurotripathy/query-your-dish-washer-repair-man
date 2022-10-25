# bs4 hacking ideas from https://stackoverflow.com/questions/34589064/beautifulsoup-get-the-class-text

import requests
from bs4 import BeautifulSoup, NavigableString, Tag


def gen_text(url, out_file):
    
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    allowlist = ['p',]


    with open(out_file, 'w') as f:
        text_elements = [t for t in soup.find_all(text=True, recursive=True) if t.parent.name in allowlist]

        for text_element in text_elements:
            f.write(f"{text_element}'\n'")

        print(f'table-of-contents')
        for div in soup.findAll('div', {'class': 'toc-category'}):
            f.write(str(div.find_all(text=True)))


    html = "<p><strong>Pancakes</strong><br/> A <strong>delicious <em>xxx</em></strong> type of food<br/></p>"

    soup = BeautifulSoup(html, 'html.parser')
    p = soup.find('p').find_all(text=True, recursive=True)
    print(p)

    html = "<p><strong>Pancakes</strong><br/> A <strong>delicious</strong> type of food<br/></p>"

    soup = BeautifulSoup(html, 'html.parser')
    text = ''
    for child in soup.find_all('p')[0]:
        if isinstance(child, NavigableString):
            text += str(child).strip()
        elif isinstance(child, Tag):
            if child.name != 'br':
                text = text + ' ' + child.text + ' '
            else:
                text += '\n'

    result = text.strip().split('\n')
    print(result)

    
    html = "<p><strong>Pancakes</strong><br/> A <strong><em> delicious</em> </strong> type of food<br/></p>"

    soup = BeautifulSoup(html, 'html.parser')
    text = ''
    for child in soup.find_all('p')[0]:
        if isinstance(child, NavigableString):
            text += str(child).strip()
        elif isinstance(child, Tag):
            if child.name != 'br' or child.name != 'em':
                text = text + ' ' + child.text + ' '
            else:
                text += '\n'

    result = text.strip().split('\n')
    print(result)

    soup = BeautifulSoup(html_text, 'html.parser')
    for i, para in enumerate(soup.findAll('p')):
        print(f'***{i}***')
        text = ' '
        for child in para:
            if isinstance(child, NavigableString):
                text += str(child).strip()
            elif isinstance(child, Tag):
                if child.name != 'br' or child.name != 'em':
                    text = text + ' ' + child.text + ' '
                else:
                    text += '\n'
        result = text.strip().split('\n')
        print(result)


# main
out_file = 'out-file.txt'   
for i in range(1, 6):
    url = f'https://www.appliancerepair.net/dishwasher-repair-{i}.html'
    gen_text(url, out_file)   
