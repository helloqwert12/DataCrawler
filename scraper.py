import scrapy
import MySQLdb
from ftfy import fix_encoding

counter = 0
class HotelSpider(scrapy.Spider):
	name = "hotel_spider"
	#start_urls = ['https://mytour.vn/c3/khach-san-tai-ho-chi-minh.html']
	start_urls = ['http://gotrip.vn/khach-san-nha-trang/']
	global counter
	def parse(self, response):
		
		# SET_SELECTOR = 'div.product-item.row'
		SET_SELECTOR = 'div.list-item-hotel.clearfix'
		global counter
		for hotel in response.css(SET_SELECTOR):
			# NAME_SELECTOR = 'h2::attr(title)'
			# ADDRESS_SELECTOR = 'p a::attr(title)'
			# RATE_SELECTOR = 'div.box-review span::text'
			# PRICE_SELECTOR = 'div.price-wrap'

			NAME_SELECTOR = 'div.col-md-7 div.title-detail h2 a::text'
			ADDRESS_SELECTOR = 'div.col-md-7 p::text'
			PRICE_SELECTOR = 'div.col-md-2.hotel-rigt-top div.price::text'
			RATE_SELECTOR = 'div.col-md-2 div.rating span::text'
			FACILITIES_SELECTOR = 'div.col-md-7 ul li::text'
			STAR_SELECTOR = 'div.col-md-7 div.title-detail span'

			name = str(hotel.css(NAME_SELECTOR).extract_first())#.encode('utf-8').decode('latin-1')
			address = str(hotel.css(ADDRESS_SELECTOR).extract_first())#.encode('utf-8').decode('latin-1')
			price = str(hotel.css(PRICE_SELECTOR).extract_first())#.encode('utf-8').decode('latin-1')
			rate = str(hotel.css(RATE_SELECTOR).extract_first())#.encode('utf-8').decode('latin-1')
			star = hotel.css(STAR_SELECTOR).extract()

			print(name, address, price, rate, len(star))

			global counter
			counter += 1
			idkey = "KSNT" + str(counter)
			print(idkey)

			yield addHotel(idkey, name, address, price, rate, str(len(star)))
				

		NEXT_PAGE_SELECTOR = '#listcathotel > div.page-nav.m-bottom > ul > li:nth-child(10) > a::attr(href)'
		next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
		if next_page:
			yield scrapy.Request(
			 	response.urljoin(next_page),
			 	callback = self.parse
			)

def addHotel(idkey, name, address, price, rate, star):
		db = MySQLdb.connect("localhost","root","","hotel_crawler", charset='utf8', use_unicode=True)
		cursor = db.cursor()

		sql = """INSERT INTO `hotel`(`MaKS`, `TenKS`, `DiaChi`, `Gia`, `XepHang`, `Sao`) VALUES(%s, %s, %s, %s, %s, %s)"""
		cursor.execute(sql, (idkey, name, address, price, rate, star))
		try:
			db.commit()
		except:
			db.rollback()

		db.close()

# addHotel("KS03", "KSHTNF", "78 Vo Thi Sau", "7.800.000", "9.0")