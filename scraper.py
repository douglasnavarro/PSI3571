import requests
import re
from bs4 import BeautifulSoup

try:
    vq_home = requests.get('http://www.viaquatro.com.br/').text
except:
    vq_home = None

if(vq_home is not None):
    s = BeautifulSoup(vq_home, 'html.parser')
else:
    s = None

def get_operation_status(soup):

    status = {
    'azul': '',
    'verde': '',
    'vermelha': '',
    'amarela': '',
    'lilás': '',
    'rubi': '',
    'diamante': '',
    'esmeralda': '',
    'turquesa': '',
    'coral': '',
    'safira': '',
    'prata': ''
    }

    status['amarela'] = soup.find('img', id="imageCurrentLineFourStatus")['alt']
    # if('normal' in status_amarela):
    #     status_amarela = 'normal'
    # elif('reduzida' in status_amarela):
    #     status_amarela = 'velocidade reduzida'
    # else:
    #     status_amarela = 'interrompida'

    stations = soup.find_all('div', class_='estacao')
    for station in stations:
        name_and_status = station.find_all('span')
        if(len(name_and_status) == 2):
            name = name_and_status[0].text.lower()
            station_status = name_and_status[1].text.lower()
            status[name] = station_status    
    return(status)

def get_time_data(soup):
    div_list = soup.findAll('div', class_='titulo-operacao')

    for div in div_list:
        h3 = div.find('h3').text
        if(h3 == 'Operação'):
            line4 = div.find('time').text
        elif(h3 == 'Metrô de São Paulo'):
            metro = div.find('time').text
        elif(h3 == 'CPTM'):
            cptm = div.find('time').text
    
    line4 = re.search(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}',line4).group()
    metro = re.search(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}',metro).group()
    cptm = re.search(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}',cptm).group()
        
    return(line4, metro, cptm)

print(get_operation_status(s))