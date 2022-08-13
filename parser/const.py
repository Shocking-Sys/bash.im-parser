from requests.structures import CaseInsensitiveDict

DB_FILE = 'quotes.sqlite3'
RETRY_ATTEMPTS = 5

HEADERS = CaseInsensitiveDict()
HEADERS['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36"