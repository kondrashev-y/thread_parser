from threading import Thread, Lock
from requests_html import HTMLSession
from time import sleep
from reppy.robots import Robots
from time import strftime, gmtime, time



domain = input('Введите домен:')
domain_link = f'https://{domain}'

new_urls = {domain_link}
scaned_urls = set()
locker = Lock()

robots = Robots.fetch(domain_link)
agent = 'Googlebot'

timestamp = strftime("__%d_%b_%H_%M_%S", gmtime())
file = open(f'{domain}_{timestamp}.txt', 'a', encoding='utf-8')


def worker():
    with HTMLSession() as session:
        while True:
            if len(new_urls) == 0:
                sleep(10)
                if len(new_urls) == 0:
                    break
            try:
                url = new_urls.pop()
                response = session.get(url, timeout=1)
                url_links = response.html.absolute_links
                title = '|'.join(response.html.xpath("//title/text()"))
                h1 = '|'.join(response.html.xpath("//h1/text()"))
                # title = ''.join(title.split()).strip()
                title = title.replace('\n', '')
                if h1:
                    h1 = ''.join(h1[0].split()).strip()
                else:
                    h1 = '-'
                with locker:
                    for link in url_links:
                        if domain not in link:
                            continue
                        if robots.allowed(domain_link, agent):
                            if '#' in link:
                                link = link[:link.index('#')]
                            if link not in scaned_urls:
                                new_urls.add(link)
                                file.write(f'{url}\t{title}\t{h1}\n')
                        else:
                            file.write(url + '\t---->\t' + 'Disallow in robots.txt\n')
                            continue
                scaned_urls.add(url)
                print(url, '----->', title)
            except Exception as e:
                print(e, type(e))


for i in range(10):
    thread = Thread(target=worker)
    thread.start()
