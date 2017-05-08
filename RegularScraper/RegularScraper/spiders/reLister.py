import scrapy

class ReLister ( scrapy.Spider ):
	name = "regularLister"

	def __init__ ( self, *args, **kwargs ):
		super ().__init__( *args, **kwargs )

		self.__urlDepth__ = {}
		with open ( 'reg.ex', 'r' ) as f:
			self.__myRegexList__ = list (filter ( lambda x : x.strip () != '', (reg.strip () for reg in f ) ))

		with open ( 'log', 'a' ) as f:
			f.write ( "regexlist = " + str ( self.__myRegexList__ ) + '\n\n' )

	def fixUrl ( self, url ):
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
			urls = list (url.strip () for url in f)

		for url in urls:
			url = self.fixUrl ( url )
			self.__urlDepth__ [ url ] = 0
			yield scrapy.Request ( url, callback = self.parse )

	def parse(self, response):
		if ( 'redirect_urls' in response.meta ):
			url = response.meta [ 'redirect_urls' ][0]
		else:
			url = response.url
		depth = self.__urlDepth__ [ url ]
		depthLim = len ( self.__myRegexList__ )

		with open ( 'log', 'a' ) as f:
			f.write ( "crawler parse\n" )
			f.write ( "url = " + response.url + '\n' )
			f.write ( "meta = " + str ( response.meta ) + '\n\n' )

		if ( depth == len ( self.__myRegexList__ ) ):
			with open ( 'result', 'a' ) as f:
				f.write ( url + '\n' )

			return

		regex = self.__myRegexList__ [ depth ]
		urls = list(url for url in response.css ( 'a::attr(href)' ).re ( regex ))

		if ( depth == depthLim - 1 ):
			with open ( 'result', 'a' ) as f:
				for nUrl in urls:
					nUrl = self.fixUrl ( nUrl )

					if ( nUrl in self.__urlDepth__ ):
						continue

					f.write ( nUrl + '\n' )
		else:
			for nUrl in urls:
				nUrl = self.fixUrl ( nUrl )

				if ( nUrl in self.__urlDepth__ ):
					continue

				self.__urlDepth__ [ nUrl ] = depth + 1
				yield scrapy.Request ( nUrl, callback = self.parse )
