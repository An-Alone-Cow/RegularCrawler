import scrapy

class ReLister ( scrapy.Spider ):
	name = "regularLister"

	__myRegexList = [];
	__urlDepth = {};

	def fixUrl ( url ):
		if ( url == '' ):
			return ''

		if ( url [ 0 ] != 'h' ):
			url = 'h' + url

		if ( url [ 1 ] != 't' ):
			url = 'ht' + url [1:]

		if ( url [ 2 ] != 't' ):
			url = 'htt' + url [2:]

		if ( url [ 3 ] != 'p' ):
			url = 'http' + url [3:]

		if ( url [ 4 ] != ':' ):
			url = 'http:' + url [4:]

		if ( url [ 5 ] != '/' ):
			url = 'http:/' + url [5:]

		if ( url [ 6 ] != '/' ):
			url = 'http://' + url [6:]

		return url


	def start_requests(self):
		with open ( 'urls.lst', 'r' ) as f:
			urls = [(url.strip () for url in f)]

		with open ( 'reg.ex', 'r' ) as f:
			__myRegexList = [(reg.strip () for reg in f )]

		for url in urls:
			url = fixUrl ( url )
			__urlDepth [ url ] = 0
			yield scrapy.Request ( url, callback = self.parse )

	def parse(self, response):
		url = response.meta [ 'redirect_urls' ][0]
		depth = __urlDepth [ url ]

		if ( depth == len ( __myRegexList ) ):
			with open ( 'result', 'a' ) as f:
				f.write ( url + '\n' )

			return

		regex = __myRegexList [ depth ]
		urls = [(url for url in response.css ( 'a::attr(href)' ).re ( regex ))]

		for nUrl in urls:
			nUrl = fixUrl ( nUrl )

			if ( nUrl in __urlDepth )
				continue

			__urlDepth [ nUrl ] = depth + 1
			yield scrapt.Request ( nUrl, callback = self.parse )
