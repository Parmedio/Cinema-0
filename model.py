sost_txt = [
  ('\ue415',''),
  ('\x88', ''),
  ('\x89', ''),
  ('\x8c', ''),
  ('Ã¸', 'ø'),
  ('Ã²', 'ò'),
  ('Ã³', 'ó'),
  ('Ã¬', 'ì'),
  ('Ã¨', 'è'),
  ('Ã§', 'ç'),
  ('nÃ¹', 'nù'),
  ('Regia di ', 'di '),
  (',durata ', ' - Durata: '),
  ('Un film con ', ' Con '),
  ('Un filmcon ', ' Con '),
  ('piÃ¹', 'più'),
  ('Ã¥', 'å'),
  ('Â', ''),
  ('Ã¶', 'ö'),
  ('tÃ', 'tà'),
  ('rÃ', 'rà'),
  ('iÃ', 'ià'),
  ('Ã©', 'é'),
  ('à©', 'é'),
  ('Ã', 'È'),
  ('È¡', 'á'),
  ('È¢', 'â'),
  (',20', ', 20'),
  (' .', '.'),
  ('\xa0', '')
]

rx_txt = [
  ('\n\s+', ''),
  ('\..*Box Office.*', '.'),
  ('Da vedere \d*', ' '),
  (',', ', '),
  ('\s{2,}', ' ')
]

rx_url = [
  ('\s+', ''),
]

save_folder = 'locandine recensioni'
list_file = 'lista url film.txt'
list_error = 'errors report'