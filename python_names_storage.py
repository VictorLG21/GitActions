from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "dataops-383600",
  "private_key_id": "991b95845d3df0feb081f6da17500c06312fe043",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDAE+5EX9mhoKdQ\nh3HoBnS47gis0FI1E4EqhdEz/rPIZW8iSvngMdW4XEEtS6SgNjdHbfC4Xe9wpGw0\n3DZol7QGy2PsU10i606ehngX5N5Yosl4c+nrBhlro6xvPkjZO17iKcFkYXw6aTPS\ngVz86b4kcinbmNpFYprwyiSgzgNvGw9hXGBDJa4tKV/jg3+5YFCnyPFp0nDn1dIq\n9AWiOUxzA/ETg2bgPCUfNkG4NJ6wj+R6eNVJxnd+gDEugUE+cXlSxGmr6U8c5TM4\nDcbjvDnmqrv16f6zaLLM1kqyT/ZMkZTDKjcCigmVJkEE3I3SSji9K18k256SLJL6\n4d4O7lFFAgMBAAECggEABqdKFsqT29eYTspPpaAU9VOi2kr3ELPwbVF9rzA7TbhH\nHWgnzV58jup8hCioIbfvD0WIKU1xCLUGszK48cOQ2WFnQIhHZCPEMT/q3g0FWgr9\nhp4hSWJd3rl933adXbpYQuZRDCdHqdr7ZWcqGkVbMEuswS4YytQrwNEya/Lm8eIY\njOUmuGlZCA6LZi/j6bORUptN8SxainTSk+rrs7okBHWGWMpBwQCmBJiiY9iqsUIS\ns0jlXjY34uI6AHHEwK0VjzEWpFKrhCnIrIc9cRNgs9V6MWqd0ruRPYqr8Yn3REwT\n6JxK4cKF2v9MDQ+bK9MrLFKxLtGxXwhUF7rMtxOxAQKBgQDg5dXTs2zfCi1wRHia\nnrnLgKFPahjB1j+5U/fO+N/mQ11Y+Tb4Zv7iINM/jFGDzQNz3DLIQhhBIXHUkYN7\nh9rwhsQnX/eNl7oja0Org1svt58/teVKCgklA5yl40mxxkXcMCp/HDdgmnmxuRbj\nhY8+U+k1awNsR4p8obwm7SC3xQKBgQDapCfGLaT8wv3ztg1O41cl8GkuvBaPm/xV\n1qWmvDyUEjHrwljsx/FizdLH7e8cQCNTsNTtplpSR9faEOxFbZvKAGIo1xBQrY+0\ntJK0QMSs+gr5kKZGHEuUDRVQz6LZC/YITE8R01UXIaycViqkB7dZ3pH2vDU1MrQ6\nijaPu99LgQKBgH654+h7xVBVCs+lNZRi9myumbcHINYw5Q2IPC4bXQcCVJprK8eD\nOgKv3nmDlvc+0cA6hz8Cx2oD74GJUV6Nahh4yBUr5XGa2p9UtPfzd7GGtayP0ZkL\n2KVLyLxNO9x5zinJ1lhzzNyZjxNPKY+hVdsYK2QXXgFouqeJ91yz5+jFAoGBANK/\ndoNFTgpB3k3DRrKq2j78rDZbIJgOsD0BaKz+Npo3q5znuZWK6LbnVGxYganGfQbX\npXbpaZh0HbDZrRUDIS6mDff1zYkmsyVpBRvwbmOZpWiHsG5WKdesgMZjTkJOkDnR\nbEnvXc6tK9eKCxIPSgG7UxD0u4jqteTTguIrIoKBAoGAcId+AjUiD5KBB4rbBokl\nPzbU7jypYJ8wifqBZcwtDVsxBc5wZEHlQ+lMC6T4wBIQKa8kkndPLcPKvf9oZ3x5\nly3LQRTPUPObyMJqZeyyhQCiauiowb49zeX22Y3FfzJf260fqGGUiXouNKzupahA\nblACNkYz8d5VvUfXmhZEt4s=\n-----END PRIVATE KEY-----\n",
  "client_email": "93639898919-compute@developer.gserviceaccount.com",
  "client_id": "107290698649754386708",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/93639898919-compute%40developer.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('weather-sp') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
