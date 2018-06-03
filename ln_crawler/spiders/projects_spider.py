import scrapy


class ProjectsSpider(scrapy.Spider):
    name = "projects"
    start_urls = [
        "https://ln.hako.re/danh-sach?page=1"
    ]

    def parse(self, response):
        for project in response.xpath('//*[@id="mainpart"]/div[2]/div[2]//article[not(contains(@class,"top"))]'):
            project_uri = project.xpath('div/a/@href').extract_first()
            print('Get info: %s' % project_uri)
            yield response.follow(project_uri, self.parse_project_detail)

        # Follow pagination links
        # next_page = response.xpath(
        #     '//footer//div[@class = "pagination_wrap"]/a[contains(@class,"current")]/following-sibling::a[1]/@href').extract_first()
        # print('next_page = %s' % next_page)
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_project_detail(self, response):
        def extract_one_xpath(expr):
            return response.xpath(expr).extract_first()

        def extract_multi_xpath(expr):
            return response.xpath(expr).extract()

        project_detail = {
            'synopsis': extract_one_xpath(
                '//*[@id="mainpart"]/section[1]/div[1]/main[1]/article[1]/div[3]/div[2]/div[1]/div[1]/p[1]/text()'),
            'author': extract_one_xpath('//*[@id="rd-sidebar"]/section[2]/div[1]/main[1]/div[2]/span[2]/a/text()'),
            'status': extract_one_xpath('//*[@id="rd-sidebar"]/section[2]/div[1]/main[1]/div[3]/span[2]/text()'),
            'genres': extract_multi_xpath('//*[@id="rd-sidebar"]/section[2]/div[1]/main[1]/div[4]/span[2]/a/text()'),
            'views': extract_one_xpath('//*[@id="rd-sidebar"]/section[2]/div[1]/main[1]/div[5]/span[2]/text()')
        }
        print('\n\n=== Author: %s' % project_detail['author'])
        yield project_detail
