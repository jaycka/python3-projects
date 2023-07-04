import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

initial_url = 'https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors'

response = requests.get(initial_url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

max_pages = int(soup.select('.pagination__btn--inner')[-2].text)
df = pd.DataFrame(columns=["Rank", "Major", "Degree Type", "Early Career Pay", "Mid-Career Pay", "% High Meaning"])

for i in tqdm(range(1, max_pages + 1)):
    url = f"https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/{i}"
    response = requests.get(url)
    try:
        response.raise_for_status()
    except:
        print(f"Page {i} not scraped")
        break
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.select('.data-table__row')
        for j in data:
            rowdata = j.find_all('span', class_='data-table__value')
            df.loc[len(df)] = [
                int(rowdata[0].text),
                rowdata[1].text,
                rowdata[2].text,
                int(rowdata[3].text.replace('$', '').replace(',', '')),
                int(rowdata[4].text.replace('$', '').replace(',', '')),
                float(int(rowdata[5].text.replace('%', '')) / 100) if rowdata[5].text != '-' else None
            ]
df.to_csv('payscale.csv')

