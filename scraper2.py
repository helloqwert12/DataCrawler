import scrapy
import MySQLdb
from ftfy import fix_encoding

counter = 0
class HotelSpider(scrapy.Spider):
	name = "hotel_spider"
	start_urls = ['http://gotrip.vn/']
	download_delay = 5
	global counter	
	def parse(self, response):
		SET_SELECTOR = '#footer > div.footer-menu > div > div'
		location = response.css(SET_SELECTOR)
		LOCATION_SELECTOR = 'ul li a::attr(href)'
		hotelList = location.css(LOCATION_SELECTOR).extract()

		for link in hotelList:
			next_page = 'http://gotrip.vn' + link
			if next_page:
					yield scrapy.Request(
					url = next_page,
					callback=self.parse2
				)
				
	def parse2(self, response):
		print("---------> spider for url: ", response.url)
		SET_SELECTOR = 'div.list-item-hotel.clearfix'
		global counter
		for hotel in response.css(SET_SELECTOR):
			NAME_SELECTOR = 'div.col-md-7 div.title-detail h2 a::text'
			ADDRESS_SELECTOR = 'div.col-md-7 p::text'
			PRICE_SELECTOR = 'div.col-md-2.hotel-rigt-top div.price::text'
			RATE_SELECTOR = 'div.col-md-2 div.rating span::text'
			FACILITIES_SELECTOR = 'div.col-md-7 ul li::text'
			STAR_SELECTOR = 'div.col-md-7 div.title-detail span'
			IMAGE_SRC_SELECTOR = 'div.col-md-3 a img::attr("src")'

			name = str(hotel.css(NAME_SELECTOR).extract_first())
			address = str(hotel.css(ADDRESS_SELECTOR).extract_first())
			price = str(hotel.css(PRICE_SELECTOR).extract_first())
			rate = str(hotel.css(RATE_SELECTOR).extract_first())
			star = hotel.css(STAR_SELECTOR).extract()
			image = str(hotel.css(IMAGE_SRC_SELECTOR).extract_first())

			print(name, address, price, rate, len(star), image)

			global counter
			counter += 1
			idkey = "KS" + str(counter)
			print(idkey)

			yield addHotel(idkey, name, address, price, rate, str(len(star)), image)
				
		NEXT_PAGE_SELECTOR = '#listcathotel > div.page-nav.m-bottom > ul > li:last-child > a::attr(href)'
		next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
		if next_page:
			return scrapy.Request(
			 	response.urljoin(next_page),
			 	callback = self.parse2
			)

def addHotel(idkey, name, address, price, rate, star, anh):
		db = MySQLdb.connect("localhost","root","","hotel_crawler", charset='utf8', use_unicode=True)
		cursor = db.cursor()

		sql = """INSERT INTO `hotel`(`MaKS`, `TenKS`, `DiaChi`, `Gia`, `XepHang`, `Sao`, `Anh`) VALUES(%s, %s, %s, %s, %s, %s, %s)"""
		cursor.execute(sql, (idkey, name, address, price, rate, star, anh))
		try:
			db.commit()
		except:
			db.rollback()

		db.close()