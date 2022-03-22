import requests
import os
from bs4 import BeautifulSoup

def remove_slug_link(rel_link, slug_len=3):
    temp = rel_link.split('/')
    return '/'.join(temp[slug_len:])

os.makedirs('papers/neurips', exist_ok=True)
downloaded_papers = os.listdir('papers/neurips')

url = input('Enter URL (https://papers.nips.cc/paper/2021): ') or 'https://papers.nips.cc/paper/2021'
soup = BeautifulSoup(requests.get(url).text, 'html.parser')

parent = soup.find('div', {'class': 'container-fluid'})
papers = parent.find_all('li')

for i, paper in enumerate(papers):
    try:

        info = paper.find('a')
        title = info.text

        if title + '.pdf' in downloaded_papers:
            continue
        
        link = remove_slug_link(info['href'])
        abs_link = url + '/' + link

        paper_page = BeautifulSoup(requests.get(abs_link).text, 'html.parser')
        buttons = paper_page.find_all('a', {'class': 'btn btn-light btn-spacer'})

        pdf_info = list(filter(lambda x: x.text == 'Paper', buttons))[0]
        link = remove_slug_link(pdf_info['href'])
        abs_link = url + '/' + link
        print(title)
        print(f'Downloading paper {i+1}/{len(papers)}', end='\r')

        pdf_file = requests.get(abs_link)
        with open(f'papers/neurips/{title}.pdf', 'wb') as f:
            f.write(pdf_file.content)
    except:
        print('Error occured')
        continue
    