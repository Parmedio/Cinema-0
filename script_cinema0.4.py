import requests as req
from bs4 import BeautifulSoup
from tqdm import tqdm
from pathlib import Path
from time import sleep
from model import sost_txt, rx_txt, rx_url, save_folder, list_file, list_error
import re

def formatta(item):
  for regex in rx_txt:
    item = re.sub(regex[0], regex[1], item)
  for sost in sost_txt:
    item = item.replace(sost[0], sost[1])
  return item

def format_url(item):
  for regex in rx_url:
    item = re.sub(regex[0], regex[1], item)
  return item

def distilla(ph1, i1, ph2 = '', i2 = None):
  if ph2 == '':
    return formatta(soup.select(f'{ph1}')[i1].getText())
  else:
    return formatta(soup.select(f'{ph1}')[i1].select(f'{ph2}')[i2].getText())

def annota(topic):
  file_dest.write(topic + '\n\n\n')

def anomalia(topic):
  errors_found.append(f'    \'sezione\': \'{topic}\',\n    \'titolo film\': \'{movie_name}\',\n    \'url film\': \'{film}\'')

with open(f'{Path().resolve()}/{list_file}', 'r') as f:
  contenuto = f.read()
  lista = contenuto.split('\n')
  array_url_film = [format_url(x) for x in lista if len(format_url(x))]

save_path = f'{Path().resolve()}/{save_folder}/'
errors_found = []
wrong_url = []
url_index = 1
min = ' minuti.'

for film in tqdm(array_url_film):
  try:
    res = req.get(film)
    soup = BeautifulSoup(res.text, 'html.parser')

    url_locandina_01 = soup.select('.mm-spazio-locandina')[0].select('amp-img')[0].get('src', None)
    locandina01 = req.get(url_locandina_01).content

    movie_name = distilla('h1', 0).upper()
    info = distilla('.sottotitolo_rec', 0)
    highlights = distilla('.highlights', 0)
    catchy = distilla('.titolo', 1, 'div', 4)
    sinossi = distilla('.corpo', 0)
    analisi_film = soup.select('.corpo')[1:4]

    with open(f'{save_path}recensione {movie_name}.txt', mode='w') as file_dest:
      annota(f'____________{movie_name}____________')
#-------------INFO-------------------------------------------------------------
      try:
        txt_info = re.search(r'.* minuti.', info)[0]
        reg_cast = re.search(r'di \D*?\.\D*?\.', txt_info)[0]
        paese_min = re.search(r'(?<=- )[^-]*$', txt_info)[0]
        annota(reg_cast + ' ' + paese_min.replace(min, '\''))
      except:
        annota(info)
        anomalia('INFO')
#-------------HIGHLIGHTS-------------------------------------------------------
      try:
          annota(highlights)
      except:
        anomalia('HIGHLIGHTS')
#-------------CATCHY-----------------------------------------------------------
      try:
        annota(catchy)
      except:
       anomalia('CATCHY')
#-------------SINOSSI----------------------------------------------------------
      try:
        annota(sinossi)
      except:
        anomalia('SINOSSI')
#-------------ANALISI----------------------------------------------------------
      try:
        for x in analisi_film:
          file_dest.write(formatta(x.getText()))
      except:
        anomalia('ANALISI')
#-------------LOCANDINA--------------------------------------------------------
    if '.jpg' in url_locandina_01:
      with open(f'{save_path}locandina - {movie_name}.jpg', 'wb') as image:
        image.write(locandina01)
  except:
    wrong_url.append(f'L\'url nr. {url_index} ({film})')
  url_index += 1

timeout = 4

if len(array_url_film) == 0:
  print('\nLista url film vuota.')

if len(errors_found) > 0:
  timeout = 10
  print(f'\nAVVISO! Si sono verificati degli errori durante il download,\nInviare il file \'{list_error}\' alla mail in calce per correggere lo script attualemtne in uso.')
  with open(f'{Path().resolve()}/{list_error}.txt', mode='w') as err_rep:
    error_count = 1
    err_rep.write('errors_found = {\n')
    for x in errors_found:
      if error_count < len(errors_found):
        err_rep.write(f'  {error_count} : ' + '{\n' + f'{x}' + '\n  },\n')
        error_count += 1
      else:
        err_rep.write(f'  {error_count} : ' + '{\n' + f'{x}' + '\n  }\n')
    err_rep.write('}')

if len(wrong_url) > 0:
  timeout = 10
  print(f'\nAVVISO! I seguenti url dei film non sono scritti correttamente:\n')
  url_count = 1
  for x in wrong_url:
    if url_count < len(wrong_url):
      print(f'-> {x};')
      url_count += 1
    else:
      print(f'-> {x}.')

print(f'\noperazione completata 👍\npowered by ~ Parmedio ~ marco.da.pieve@gmail.com')
sleep(timeout)