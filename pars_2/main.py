from requests_html import HTMLSession
from time import strftime, gmtime
from concurrent.futures import ThreadPoolExecutor


pages = []

base_link = 'https://seoprofy.ua/blog/page/'
for i in range(1, 72):
    pages.append(base_link+str(i))


session = HTMLSession()

agent = 'Googlebot'

timestamp = strftime("__%d_%b_%H_%M_%S", gmtime())
file = open(f'new_resalt{timestamp}.txt', 'a', encoding='utf-8')


def worker(url):
    response = session.get(url, timeout=1)

    links = response.html.xpath('//article[@class="article article__note"]/a[1]/@href')
    names = response.html.xpath('//article[@class="article article__note"]//h2/text()')
    dates = response.html.xpath('//article[@class="article article__note"]//time/@datetime')

    result = zip(links, names, dates)
    print('SUCCESS', url)
    return list(result)


with ThreadPoolExecutor(max_workers=20) as executor:
    result = executor.map(worker, pages)

all_articles = []
for item in result:
    all_articles += item

with open(f'new_resalt{timestamp}.txt', 'a', encoding='utf-8') as file:
    for i in all_articles:
        file.write(f'{i[0]}\t{i[1]}\t{i[2]}\n')

# with ThreadPoolExecutor(max_workers=20) as executor:
#     all_results = []
#     for lk in pages:
#         future = executor.submit(worker, lk)
#         all_results.append(future)
#
# for future in all_results:
#     print(future.result())
