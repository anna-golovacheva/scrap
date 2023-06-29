BASE_URL = 'https://goldapple.ru/parfjumerija?p='
BASE_PRODUCT_URL = 'https://goldapple.ru'
PAGES = 11

TAG = 'article'

USAGE_FIRST_REGEXP = r'(?<=text:"применение")(.*?)(?=},)'
USAGE_SECOND_REGEXP = r'(?<=content:")(.*?)(?=")'
DESCRIPTION_FIRST_REGEXP = r'(?<=text:"описание")(.*?)(?=,attributes)'
DESCRIPTION_SECOND_REGEXP = r'(?<=content:")(.*?)(?=")'
COUNTRY_FIRST_REGEXP = r'(?<=страна происхождения)(.*?)(?=изготовитель)'
COUNTRY_SECOND_REGEXP = r'([аА-яЯ]{3,})'
