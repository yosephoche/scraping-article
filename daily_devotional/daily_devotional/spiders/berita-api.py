import scrapy
import json

class ToScrapeSpiderAPI(scrapy.Spider):
    name = 'berita-api'
    url = 'https://www.alkitab.or.id/api/get-news'
    limit = None

    # start_urls = [
    #     'https://www.alkitab.or.id/api/get-news'
    # ]

    def start_requests(self):
        limit = getattr(self, 'limit', None)

        if limit is not None:
            self.limit = limit
            url = f'{self.url}?limit={limit}&offset={limit}'
        
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        api_response = json.loads(response.text)
        for berita in api_response["data"]:
            yield {
                "id": berita["id"],
                "url": berita["url"],
                "title": berita["title"],
                "description": berita["excerpt"],
                "slug": berita["slug"],
                "thumb_image_url": berita["image_s"],
                "full_image_url": berita["image_l"],
                "published_date": berita["published_date"],
                "tags": berita["tags"]
            }

        next_page_url = api_response["paging"]["offset"]
        if next_page_url is not None:
            url = f"{self.url}?offset={next_page_url}"
            # if self.limit is not None:
            #     url = f"{self.url}&?offset={next_page_url}"
            yield scrapy.Request(url)