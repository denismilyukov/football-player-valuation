import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
import random


pd.options.display.max_columns = 37
pd.set_option('display.width', None)

user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
    ]

def convert_to_millions(match):
    amount = float(match.group(1))
    unit = match.group(2)

    if unit == 'тыс':
        amount /= 1000  # преобразуем тысячи в миллионы

    return str(amount)

def make_safe_request(url, delay=3):
    headers = {
        "User-Agent":random.choice(user_agents)
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code!=200:
        time.sleep(delay)
        make_safe_request(url, delay+1)
    return response




leagues = {
   # 'Испании':'ES1',
   #  'Италии':'IT1',
   #  'Германии':'L1',
   #  'Франции':'FR1',
   #  'Голландии':'NL1',
   #  'Бельгии':'BE1',
   #  'России':'RU1',
   #  'Португалии':'PO1',
    'Бразилии':'BRA1',
    # 'Англии':'GB1'
}

club_lists = {
    'ES1':['Real Madrid', 'Barcelona', 'Atlético Madrid', 'Athletic Club', 'Real Sociedad', 'Betis','Villarreal', 'Valencia',
           'Sevilla', 'Girona', 'Celta Vigo', 'Las Palmas', 'Espanyol', 'Osasuna', 'Alavés', 'Getafe', 'Mallorca',
           'Valladolid', 'Rayo Vallecano', 'Leganés'],
    'IT1':['Inter', 'Juventus', 'Milan', 'Atalanta', 'Napoli', 'Roma', 'Fiorentina', 'Bologna', 'Lazio', 'Torino', 'Como', 'Udinese',
           'Genoa', 'Parma', 'Lecce', 'Hellas Verona', 'Empoli', 'Monza', 'Venezia', 'Cagliari'],
    'L1':['Bayern Munich', 'Leverkusen', 'RB Leipzig', 'Dortmund', 'Eint Frankfurt', 'Stuttgart', 'Wolfsburg', 'Gladbach',
          'Hoffenheim', 'Freiburg', 'Mainz 05', 'Augsburg', 'Union Berlin', 'Werder Bremen', 'Heidenheim', 'St. Pauli',
          'Bochum', 'Holstein Kiel'],
    'FR1':['Paris S-G', 'Monaco', 'Marseille', 'Lille', 'Lyon', 'Strasbourg', 'Rennes', 'Nice', 'Lens', 'Reims', 'Toulouse',
           'Nantes', 'Brest', 'Auxerre', 'Saint-Étienne', 'Le Havre', 'Montpellier', 'Angers'],
    'NL1':['Feyenoord', 'PSV Eindhoven', 'Ajax', 'AZ Alkmaar', 'Twente', 'Utrecht', 'Heerenveen', "Sparta R'dam", 'Go Ahead Eag',
           'NEC Nijmegen', 'Groningen', 'Zwolle', 'Fortuna Sittard', 'NAC Breda', 'Heracles Almelo', 'Almere City', 'Willem II',
           'RKC Waalwijk'],
    'BE1':['Club Brugge', 'Genk', 'Union SG', 'Anderlecht', 'Gent', 'Antwerp', 'Westerlo', 'Standard Liège', 'Cercle Brugge',
           'OH Leuven', 'Charleroi', 'Mechelen', 'Sint-Truiden', 'Kortrijk', 'Dender', 'Beerschot'],
    'PO1':['Sporting CP', 'Porto', 'Benfica', 'Braga', 'Vitoria', 'Famalicão', 'Rio Ave', 'Estoril', 'Santa Clara', 'Arouca',
           'Gil Vicente FC', 'Casa Pia', 'Moreirense', 'Farense', 'Estrela', 'Nacional', 'AVS Futebol', 'Boavista'],
    'BRA1':['Flamengo', 'Palmeiras', 'Corinthians', 'Botafogo (RJ)', 'Atlético Mineiro', 'Internacional', 'São Paulo',
            'Vasco da Gama', 'Cruzeiro', 'Fluminense', 'Grêmio', 'Bahia', 'RB Bragantino', 'Ath Paranaense', 'Fortaleza',
            'Atl Goianiense', 'Criciúma', 'Vitoria', 'Cuiabá', 'Juventude'],
    'GB1':['Manchester City', 'Chelsea', 'Arsenal', 'Liverpool', 'Manchester Utd', 'Tottenham', 'Aston Villa', 'Newcastle Utd',
           'Brighton', 'Crystal Palace', 'Bournemouth', "Nott'ham Forest", 'Wolves', 'Brentford', 'West Ham', 'Everton', 'Fulham',
           'Southampton', 'Ipswich Town', 'Leicester City']
}

for country in leagues:
    url = f'https://www.transfermarkt.world/laliga/startseite/wettbewerb/{leagues[country]}/plus/?saison_id=2024'
    if leagues[country] == 'BRA1':
        url = url[:-1] + '3'
    response = make_safe_request(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    target_div = soup.find('div', id='yw1')
    target_tds = target_div.find_all('td', class_='hauptlink')
    club_ids = []
    for td in target_tds:
        link = td.find('a')
        href = link.get('href')
        folders = href.split('/')
        club_ids.append(folders[4])

    print(f'Клубы чемпионата {country}:')
    print(club_ids)

    time.sleep(10)

    for i, club in enumerate(club_ids):
        url = f'https://www.transfermarkt.world/fc-chelsea/startseite/verein/{club}/saison_id/2024'
        if leagues[country] == 'BRA1':
            url = url[:-1] + '3'
        response = make_safe_request(url)

        print(response.status_code)
        html = response.text

        frames = pd.read_html(html)
        df = frames[1]

        for j in range(1, len(df), 3):
            df = df.drop(j)
            df = df.drop(j+1)
        df = df.reset_index()
        del df['index']
        print(df)

        df = df[['Игрок(и)', 'Стоимость']]
        df = df.rename(columns={'Игрок(и)':'Player', 'Стоимость':'Value'})
        df['Player'] = df['Player'].str.replace(r'[А-ЯЁа-яё\.]', '', regex=True)
        df['Value'] = df['Value'].str.replace(',', '.')
        df['Value'] = df['Value'].str.replace(r'(\d+(?:\.\d+)?)\s*(тыс|млн)\s*€', convert_to_millions, regex=True)
        df['Value'] = df['Value'].str.replace('-', '0')

        df['Squad'] = [club_lists[leagues[country]][i]]*len(df)

        df['Value'] = df['Value'].astype('float')
        df['Player'] = df['Player'].astype('str')
        df['Squad'] = df['Squad'].astype('str')

        print(df)
        print(df.info())

        if i == 0:
            df.to_csv(f'../data/raw/values/{leagues[country]}_players_values_24-25.csv', index=False)
        else:
            values = pd.read_csv(f'../data/raw/values/{leagues[country]}_players_values_24-25.csv')
            values = pd.concat([values, df])
            values.to_csv(f'../data/raw/values/{leagues[country]}_players_values_24-25.csv', index=False)

        time.sleep(15)
    values = values.drop_duplicates()
    print(values)
    values.to_csv(f'../data/raw/values/{leagues[country]}_players_values_24-25.csv', index=False)
