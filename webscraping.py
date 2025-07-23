
import requests
from bs4 import BeautifulSoup
import pandas as pd
import math

try:
    from google.colab import data_table
    data_table.enable_dataframe_formatter()
    USE_COLAB = True
except:
    USE_COLAB = False

def find_no_of_jobs(job):
    req = requests.get('https://wuzzuf.net/search/jobs/?a=hpb&q=' + job.replace(' ', '%20'))
    soup = BeautifulSoup(req.content, 'lxml')
    jobs_tag = soup.find('strong')
    jobs = int(jobs_tag.text.replace(',', '')) if jobs_tag else 0
    pages = math.ceil(jobs / 15)
    return jobs, pages

def scrap_pages(query):
    num_jobs, num_pages = find_no_of_jobs(query)
    query_url = query.replace(' ', '%20')

    titles_lst, links_lst, occupations_lst, companies_lst, specs_lst = [], [], [], [], []
    location_lst, company_address_lst = [], []

    for pageNo in range(num_pages):
        print(f" Scraping page {pageNo + 1} of {num_pages}...")
        url = f'https://wuzzuf.net/search/jobs/?a=hpb&q={query_url}&start={pageNo * 15}'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')

        jobs = soup.find_all("div", {'class': 'css-pkv5jc'})

        for job in jobs:
            title_tag = job.find("h2", {'class': 'css-m604qf'})
            titles_lst.append(title_tag.a.text.strip() if title_tag and title_tag.a else '')
            links_lst.append('https://wuzzuf.net' + title_tag.a['href'] if title_tag and title_tag.a else '')

            occ_tag = job.find("div", {'class': 'css-1lh32fc'})
            occupations_lst.append(occ_tag.text.strip() if occ_tag else '')

            company_tag = job.find("a", {'class': 'css-17s97q8'})
            companies_lst.append(company_tag.text.strip() if company_tag else '')

            company_info = job.find("div", {'class': 'css-d7j1kk'})
            if company_info:
                spans = company_info.find_all('span', {'class': 'css-5wys0k'})
                company_address_lst.append(spans[0].text.strip() if spans else '')
            else:
                company_address_lst.append('')

            specs_tag = job.find("div", {'class': 'css-y4udm8'})
            specs_lst.append(specs_tag.text.strip() if specs_tag else '')

            location_tag = job.find("span", {'class': 'css-5wys0k'})
            location_lst.append(location_tag.text.strip() if location_tag else '')

    scraped_data = {
        'Title': titles_lst,
        'Link': links_lst,
        'Occupation': occupations_lst,
        'Company': companies_lst,
        'Specs': specs_lst,
        'Location': location_lst,
        'Company Address': company_address_lst
    }

    df = pd.DataFrame(scraped_data)
    return scraped_data, df


job = input(" Enter job title to search on Wuzzuf: ")
data, df = scrap_pages(job)

print("\n Job Results (All):")
if USE_COLAB:
    data_table.DataTable(df)
else:
    print(df.to_string(index=False))


df.to_csv(f"{job.replace(' ', '_')}_wuzzuf_jobs.csv", index=False)

job = input(" Enter job title to search on Wuzzuf: ")
data, df = scrap_pages(job)

print("\n Job Results Table:")

if USE_COLAB:
    from google.colab import data_table
    data_table.DataTable(df)
else:
    print(df.to_string(index=False))


csv_file = f"{job.replace(' ', '_')}_wuzzuf_jobs.csv"
df.to_csv(csv_file, index=False)
print(f"\n Saved to: {csv_file}")