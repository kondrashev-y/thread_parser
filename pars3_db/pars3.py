import sys
from time import sleep, time
from queue import Queue
from requests_html import HTMLSession
from concurrent.futures import ThreadPoolExecutor
from reppy.robots import Robots


def worker(queue, robots, scaned, domain):
    session = HTMLSession()

    while True:
        if queue.empty():
            sleep(10)
            if queue.empty():
                break
        try:
            url = queue.get()
            t1 = time()
            response = session.get(url)
            t2 = time()

            title = ''.join(response.html.xpath('//title/text()')).strip()
            h1 = ''.join(response.html.xpath('//h1/text()')).strip()
            description = ''.join(response.html.xpath('//meta[@name="description"]/@content')).strip()

            load_time = round(t2-t1, 2)
            page_size = len(response.text)

            all_links = response.html.absolute_links

            # db_connection.

        except:
            pass





    # response = session.get(url)