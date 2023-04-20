from bs4 import BeautifulSoup
from datetime import datetime
import boto3
import csv

s3 = boto3.client('s3')
now = datetime.now()
date = now.strftime('%Y-%m-%d')
newspapers = ['el_tiempo', 'el_espectador']
filename = f'content-{date}.csv'
link_head_el_tiempo = 'https://www.eltiempo.com'
link_head_el_espectador = 'https://www.elespectador.com'

response_tiempo = s3.get_object(
    Bucket='headlines-raw',
    Key=f'el_tiempo/contenido-{date}.html'
)

response_espectador = s3.get_object(
    Bucket='headlines-raw',
    Key=f'el_espectador/contenido-{date}.html'
)

doc_el_tiempo = response_tiempo['Body'].read().decode('utf-8')
doc_el_espectador = response_espectador['Body'].read().decode('utf-8')


def extract_tiempo(doc_el_tiempo, filename):
    soup = BeautifulSoup(doc_el_tiempo, 'html.parser')
    headlines = soup.find_all(class_='title page-link')
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['categoria', 'titular', 'enlace'])
        for headline in headlines:
            title = headline.text
            headless_link = headline['href']
            category = headless_link.split('/')[1]
            full_link = f'{link_head_el_tiempo}{headless_link}'
            csv_writer.writerow([category, title, full_link])
    with open(filename, 'r') as csv_file:
        s3.put_object(
            Bucket='headlines-final',
            Key=f'el_tiempo/{filename}',
            Body=csv_file.read()
        )


def extract_espectador(doc_el_espectador, filename):
    soup = BeautifulSoup(doc_el_espectador, 'html.parser')
    headlines = soup.find_all("h2", class_="Card-Title Title Title")
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['categoria', 'titular', 'enlace'])
        for headline in headlines:
            title = headline.text
            headless_link = headline.find("a")["href"]
            category = headless_link.split('/')[1]
            full_link = f'{link_head_el_espectador}{headless_link}'
            csv_writer.writerow([category, title, full_link])
    with open(filename, 'r') as csv_file:
        s3.put_object(
            Bucket='headlines-final',
            Key=f'el_espectador/{filename}',
            Body=csv_file.read()
        )


extract_tiempo(doc_el_tiempo, filename)
extract_espectador(doc_el_espectador, filename)
