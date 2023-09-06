import requests
from bs4 import BeautifulSoup

url = 'https://www.nbkr.kg/index.jsp?lang=RUS'

response = requests.get(url=url)
soup = BeautifulSoup(response.text, 'lxml')
currency_rates = soup.find_all('td', class_='exrate')

all_rates = []

for currency in currency_rates:
    all_rates.append(currency.text)

# Преобразуйте строки в числа с плавающей точкой
USD_KGS = float(all_rates[0].replace(',', '.'))  # Заменяем запятую на точку и преобразуем в число
EURO_KGS = float(all_rates[1].replace(',', '.'))
RUB_KGS = float(all_rates[2].replace(',', '.'))
KZT_KGS = float(all_rates[3].replace(',', '.'))


# Теперь USD_KGS, EURO_KGS, RUB_KGS, и KZT_KGS - числа с плавающей точкой
