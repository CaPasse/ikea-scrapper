import gevent
import gevent.queue
import requests
import json

from bs4 import BeautifulSoup
from gevent.monkey import patch_all

patch_all()

class ProductFinder:

    SLEEP_TIME = 0.2

    visited = set()
    queue = gevent.queue.Queue()

    products = []

    def __init__(self, root_page):
        self.queue.put(root_page)

    def worker(self):
        while True:
            url = self.queue.get()
            gevent.spawn(self.process, url)
            gevent.sleep(self.SLEEP_TIME)

    def run(self):
        worker = gevent.spawn(self.worker)
        gevent.joinall([worker])

    def handle_product(self, product): pass

    def process(self, url):

        print("Processing " + url)

        r = requests.get(url)
        if r.status_code != 200:
            print("Cannot get page {} // {}".format(url, r.status_code))
            return

        self.visited.add(url)

        content = r.text

        product = self.get_product(content)
        if product:
            print("Found product in " + url)
            self.products.append(product)
            self.handle_product(product)

        soup = BeautifulSoup(content, "html.parser")
        for link in soup.find_all("a"):
            url = link.get("href")
            if not url:
                continue

            if url.startswith("#") or "ikea" not in url:
                continue

            if not url.startswith("http"):
                url = "http://www.ikea.com" + url

            if "#" in url:
                url = url.split('#')[0]

            if url not in self.visited:
                self.queue.put(url)

    def get_product(self, content):
        if "jProductData" not in content: return None

        content = content.split('var jProductData = ')[1].split('};')[0] + '}'
        print(content)
        return json.loads(content)


if __name__ == "__main__":
    root = "http://www.ikea.com/fr/fr/catalog/allproducts/"
    p = ProductFinder(root)
    p.run()
