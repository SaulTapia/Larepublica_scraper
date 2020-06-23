import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '/html/body//h2[@class="headline"]/a/@href'
XPATH_TITLE = '/html/body//h1[@class="headline"]/a/text()'
XPATH_SUMMARY = '/html/body//div[@class="lead"]/p/text()'
XPATH_BODY = '/html/body//div[@class="articleWrapper  "]/p[not(@class)]/text()'

def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code != 200:
            raise ValueError(f'Error. Status code {response.status_code}')
        else:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return 
            
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
    except ValueError as e:
        print(e)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_news = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_news:
                parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as e:
        print(e)


def run():
    parse_home()


if __name__ == "__main__":
    run()