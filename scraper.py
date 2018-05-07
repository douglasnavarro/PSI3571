import requests
import re
from bs4 import BeautifulSoup
import time
import logging

lines_metro = ['azul', 'verde', 'vermelha', 'amarela', 'lilas', 'prata']
lines_cptm  = ['rubi', 'diamante', 'esmeralda', 'turquesa', 'coral', 'safira']


file_handler = logging.FileHandler('log.txt', mode='a')
logger = logging.getLogger(__name__)
file_formatter = logging.Formatter(fmt='[%(asctime)s] [%(levelname)-4s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logging.basicConfig(level=logging.DEBUG)
logger.info('Starting scraper')

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

    status_amarela = soup.find('img', id="imageCurrentLineFourStatus")['alt']
    if(status_amarela == 'Operação Normal'):
        status_amarela = 'normal'
    status['amarela'] = status_amarela
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
    status['lilas'] = status['lilás']
    del status['lilás']
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
        
    return {'line4':line4, 'metro':metro, 'cptm':cptm}

while(True):

    try:
        vq_home = requests.get('http://www.viaquatro.com.br/')
        if(vq_home.status_code == 200):
            vq_home = vq_home.text
        else:
            vq_home = None
            continue
    except:
        vq_home = None
        continue

    
    s = BeautifulSoup(vq_home, 'html.parser')
    times = get_time_data(s)
    op_status = get_operation_status(s)

    with open('data.txt', 'a') as d:
        for line in lines_metro:
            if(line == 'amarela'):
                d.write('{},{},{}\n'.format(times['line4'],line, op_status[line]))
            else:
                d.write('{},{},{}\n'.format(times['metro'], line, op_status[line]))
        for line in lines_cptm:
            d.write('{},{},{}\n'.format(times['cptm'],line, op_status[line]))
    
    logger.info('Sleeping for 120 seconds')
    time.sleep(120)
    
