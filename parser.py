import requests
from bs4 import BeautifulSoup, NavigableString, Tag

def gen_text():
    pass

for i in range(1,6):
    url = f'https://www.appliancerepair.net/dishwasher-repair-{i}.html'
    gen_text()   
html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'html.parser')
# print(soup)


# print(f'iterate thru all the hyper links in the page')
# for link in soup.find_all('a'):
#     print(link.get('href'))

# print(f'all p')
# for i, para in enumerate(soup.findAll('p')):
#     print(f'***{i}***')
#     para.get_text()
#     print(para)

# # all_ps = soup.findAll('p')
# # print(f'all ps:\n {all_ps}')

# allowlist = [
#   'p',
#   'strong',
#   'em'
# ]

allowlist = [
  'p',
]


out_file = 'out-file.txt'
with open(out_file, 'w') as f:
    text_elements = [t for t in soup.find_all(text=True, recursive=True) if t.parent.name in allowlist]

    for text_element in text_elements:
        f.write(f"{text_element}'\n'")

    print(f'table-of-contents')
    for div in soup.findAll('div', {'class': 'toc-category'}):
        f.write(str(div.find_all(text=True)))


from bs4 import BeautifulSoup, NavigableString, Tag

html = "<p><strong>Pancakes</strong><br/> A <strong>delicious <em>xxx</em></strong> type of food<br/></p>"

soup = BeautifulSoup(html, 'html.parser')
p = soup.find('p').find_all(text=True, recursive=True)
print(p)


from bs4 import BeautifulSoup, NavigableString, Tag

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

# bs4 hacking ideas from https://stackoverflow.com/questions/34589064/beautifulsoup-get-the-class-text

from bs4 import BeautifulSoup, NavigableString, Tag

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