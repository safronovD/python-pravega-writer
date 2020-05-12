from ../Connector/NewsLoader import NewsLoader

Class NewsLoaderLobrary()
	
	def __init__(self):
		self._loader = NewsLoader()
		self._correct_load = 0

	def load_data(self):
		self._loader.load()


	 def result_should_be(self, expected):
        if self._result != expected:
            raise AssertionError('%s != %s' % (self._result, expected))