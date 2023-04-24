import boto3
import requests
from datetime import datetime


s3 = boto3.client('s3')
urls = ['https://www.eltiempo.com/',
        'https://www.elespectador.com/']

newspapers = ['el_tiempo', 'el_espectador']

# Fecha actual
now = datetime.now()
date = now.strftime('%Y-%m-%d')

for url, newspaper in zip(urls, newspapers):
    response = requests.get(url)
    html_content = response.text
    s3.put_object(
        Bucket='headlines-raw',
        Key=f'{newspaper}/contenido-{date}.html',
        Body=html_content
        )
