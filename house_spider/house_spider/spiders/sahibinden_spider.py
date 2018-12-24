import scrapy
import json


class SahibindenSpider(scrapy.Spider):
    name = "sahibinden"

    def start_requests(self):
        urls = [
            "https://www.sahibinden.com/satilik/ankara"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'links.json'
        links = response.css("a.classifiedTitle::attr(href)").extract()
        links = [response.urljoin(link) for link in links]

        with open(filename, 'r') as f:
            try:
                old = json.load(f)
            except json.JSONDecodeError:
                old = []
            f.close()
            links += old

        with open(filename, 'w') as f:
            json.dump(links, f, indent=4, sort_keys=True)
            f.close()
        self.log('Saved file %s' % filename)
        next_link = response.css("a.prevNextBut::attr(href)")[-1]
        if next_link is not None:
            yield response.follow(next_link, callback=self.parse)
