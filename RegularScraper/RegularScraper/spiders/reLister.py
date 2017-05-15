import scrapy
from RegularScraper.variables import Meta

def addHttp ( url ):
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

def absolutizeUrl ( response, url ):
	if ( url.split ( '/' )[ 0 ].find ( '.' ) != -1 and url [ 0 ] != '.' ):
		return addHttp ( url )

	return response.urljoin ( url )

class ReLister ( scrapy.Spider ):
	name = "regularLister"

	def __init__ ( self, *args, **kwargs ):
		super ().__init__( *args, **kwargs )

		self.__urlDepth__ = {}
			myRegexList

	def start_requests(self):
		for url in Meta.startUrls:
			url = addHttp ( url )
			self.__urlDepth__ [ url ] = 0
			yield scrapy.Request ( url, callback = self.parse, cookies = Meta.cookies )

	def parse(self, response):
		if ( 'redirect_urls' in response.meta ):
			url = response.meta [ 'redirect_urls' ][0]
		else:
			url = response.url
		depth = self.__urlDepth__ [ url ]
		depthLim = len ( Meta.regexList )

		regex = Meta.regexList [ depth ]
		urls = list(url for url in response.css ( 'a::attr(href)' ).re ( regex ))

		if ( depth == depthLim - 1 ):
			with open ( 'result', 'a' ) as f:
				for nUrl in urls:
					nUrl = addHttp ( absolutizeUrl ( response, nUrl ) )

					if ( nUrl in self.__urlDepth__ ):
						continue

					f.write ( nUrl + '\n' )
		else:
			for nUrl in urls:
				nUrl = addHttp ( absolutizeUrl ( response, nUrl ) )

				if ( nUrl in self.__urlDepth__ ):
					continue

				self.__urlDepth__ [ nUrl ] = depth + 1
				yield scrapy.Request ( nUrl, callback = self.parse, cookies = Meta.cookies )
