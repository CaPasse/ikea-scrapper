# Ikea Scrapper

Crawls Ikea's website and extracts a product whenever it encounters one. The `ProductFinder` class implements a `get_product` method and a `run` one. The `get_product` method tries to find a product in a page. The `run` method launches the crawler. Once a product is found, it is casted to `ProductFinder.handle_product` method.

## Install

Run `pip3 install -r requirements.txt`.

## Launch

`python3 product_finder.py`
