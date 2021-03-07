import scrapy
import logging


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    start_urls = [
        'http://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath("//tbody/tr")
        for country in countries:
            n = country.xpath("./td[2]/a/text()").get()
            l = country.xpath("./td[2]/a/@href").get()

            yield response.follow(url=l, callback=self.parse_country, meta={"country_name": n})

    def parse_country(self, response):
        country_name = response.request.meta["country_name"]
        rows = response.xpath(
            '(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        for row in rows:
            year = row.xpath("./td[1]/text()").get()
            pop = row.xpath("./td[2]/strong/text()").get()
            pops = row.xpath("./td[11]/text()").get()

            yield{
                "country_name": country_name,
                "year": year,
                "population": pop,
                "population_share": pops
            }
