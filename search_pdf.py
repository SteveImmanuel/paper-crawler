import os
from tika import parser

paper_folder = input('Paper directory: ')
keywords = input('Keywords (comma separated): ').split(',')

papers = os.listdir(paper_folder)
for i, paper in enumerate(papers):
    try:
        raw = parser.from_file(os.path.join(paper_folder, paper))
        
        for keyword in keywords:
            if keyword in raw['content'].lower():
                print(f'{paper} -> found ({keyword})')

        print(f'Searching {i+1}/{len(papers)}', end='\r')
    except Exception as e:
        print(f'Error occured on {paper}: {e}')