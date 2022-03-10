
# script = """
#         function main(splash)
#           splash:init_cookies(splash.args.cookies)
#           assert(splash:go{
#             splash.args.url,
#             headers=splash.args.headers,
#             http_method=splash.args.http_method,
#             body=splash.args.body,
#             })
#           assert(splash:wait(15))

#           local entries = splash:history()
#           local last_response = entries[#entries].response
#           return {
#             url = splash:url(),
#             headers = last_response.headers,
#             http_status = last_response.status,
#             cookies = splash:get_cookies(),
#             html = splash:html(),
#           }
#         end
#     """

import scrapy
from scrapy_splash import SplashRequest
import datetime

 
 
class TaobaoSpider(scrapy.Spider):
    name = 'arz_spider'
    allowed_domains = ['arizona-rp.com']
    script = '''
        function main(splash, args)
            url = args.url
            assert(splash:go(url))
            return splash:html()
        end
    '''
    def start_requests(self):
        yield SplashRequest(url='https://arizona-rp.com/servers/', callback=self.parse, endpoint='render.html', args={
            'lua_source': self.script,
            'wait': 10,
            # 'headers': {'User-Agent': 'Mozilla/5.0'}
            })
 
 
    def parse(self, response):
        # print(response.url)
        # # 1-20
        # print(response.css("div.all-servers h1::text").get())
        now = datetime.datetime.now()
        for number_server in range(1, 21):
            yield {
                'date_time': now.strftime("%d-%m-%Y %H:%M"),
                'server_name': response.css(f"div.all-servers__wrap div.server-{str(number_server)} div.mon-server__name::text").get(),
                'server__players': response.css(f"div.all-servers__wrap div.server-{str(number_server)} div.mon-server__players::text").get() + 'из 1000',
                'server__ip': response.css(f"div.all-servers__wrap div.server-{str(number_server)} div.mon-server__ip::text").get(),
                'server_vk': response.css(f"div.all-servers__wrap div.server-{str(number_server)} a.mon-server__button::attr(href)").get()

            }




