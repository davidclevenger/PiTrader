import os
try:
	import requests
except:
	raise ImportError("Please install requests before proceeding.\n"
					  "Run \"pip install requests\"")

class Robinhood:
	def __init__(self, username = None, password = None, id = None):

		self.username = None
		self.password = None
		self.id = None

		self.headers = {
			"Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "X-Robinhood-API-Version": "1.0.0",
            "Connection": "keep-alive",
            "User-Agent": "Robinhood/823 (iPhone; iOS 7.1.2; Scale/2.00)"
		}

		if username is None and password is None and id is None:
			home = os.path.expanduser("~")
			authfile = os.path.join(home,'.rhauth')
			if os.path.exists(authfile):
				try:
					f = open(authfile)
					un = f.readline()
					pw = f.readline()
					id = f.readline()
					un = un.lstrip('user=')
					pw = pw.lstrip('pass=')
					id = id.lstrip('id=')
					un = un.strip('\n')
					pw = pw.strip('\n')
					id = id.strip('\n')
					f.close()

					self.username = un
					self.password = pw
					self.id = id


				except:
					raise IOError('Unable to open or parse rh.auth!')
			else:
				raise ValueError('No username and password provided and rh.auth not found!')

		else:
			self.username = username
			self.password = password

		self.token = None
		self.account_url = 'https://api.robinhood.com/accounts/' + self.id + '/'


	def connect(self):
		"""
		Generate authorization token
		"""
		payload = {
			'client_id': 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS',
			'expires_in': 86400,
			'grant_type': 'password',
			'password': self.password,
			'scope': 'internal',
        	'username': self.username
		}

		r = requests.post('https://api.robinhood.com/oauth2/token/', data=payload)
		if r.status_code != 200:
			raise ConnectionError('Unable to establish connection with Robinhood API.')

		ret = r.json()
		self.token = ret['access_token']

	def close(self):
		"""
		Invalidate authorization token.
		"""
		auth = {'Authorization': 'Token {}'.format(self.token)}
		r = requests.post('https://api.robinhood.com/api-token-logout/', headers=auth)
		if r.status_code != 200:
			raise Warning('Logout operation was unsuccessful!')

	@staticmethod
	def get_instrument(symbol):
		"""
		Get the instrument URL.
		"""
		data = {'symbol': symbol}
		r = requests.get('https://api.robinhood.com/instruments/', data)
		if r.status_code != 200:
			raise Warning('Unable to get instrument id.')

		ret = r.json()
		return 'https://api.robinhood.com/instruments/' + ret['results'][0]['id'] + '/'

	def getBid(self, symbol):
		"""
		Get the bid price for the symbol.
		"""
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer {}'.format(self.token)
		}
		r = requests.get('https://api.robinhood.com/quotes/{}/'.format(symbol), headers=headers)
		if r.status_code != 200:
			raise Warning('Unable to retrieve bid price')

		ret = r.json()
		return float(ret['bid_price'])

	def getAsk(self, symbol):
		"""
		Get the ask price for the symbol
		"""
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer {}'.format(self.token)
		}
		r = requests.get('https://api.robinhood.com/quotes/{}/'.format(symbol), headers=headers)
		if r.status_code != 200:
			raise Warning('Unable to retrieve ask price')

		ret = r.json()

		return float(ret['ask_price'])

	def order(self, symbol, type, time_in_force, trigger, price, quantity, side, stop_price = None,
			  client_id=None, extended_hours=None, override_day_trade_checks=None, override_dtbp_checks=None):
		"""
		Abstract order interface
		"""
		instrument_url = self.get_instrument(symbol)
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer {}'.format(self.token)
		}

		order = {
			'account': self.account_url,
			'instrument': instrument_url,
			'symbol': symbol,
			'type': type,
			'time_in_force': time_in_force,
			'trigger': trigger,
			'price': price,
			'stop_price': stop_price,
			'quantity': quantity,
			'side': side
		}

		if trigger == 'stop':
			if stop_price is None:
				raise ValueError('Trigger \'stop\' requires stop_price.')
			order['stop_price'] = stop_price

		if client_id is not None:
			order['client_id'] = client_id

		if extended_hours is not None:
			order['extended_hours'] = extended_hours

		if override_day_trade_checks is not None:
			order['override_day_trade_checks'] = override_day_trade_checks

		if override_dtbp_checks is not None:
			order['override_dtbp_checks'] = override_dtbp_checks

		r = requests.post('https://api.robinhood.com/orders/', headers=headers, data=order)
		if r.status_code != 201:  # 201: Created (Success)
			raise Warning("Unable to execute order")

	def market_buy(self, symbol, quantity, price = None):
		"""
		Market buy
		"""
		if price is None:
			price = round(self.getAsk(symbol) * 1.01, 2)
		self.order(symbol, 'market', 'gtc', 'immediate', price, quantity, 'buy')

	def market_sell(self, symbol, quantity, price = None):
		"""
		Market sell
		"""
		if price is None:
			price = round(self.getBid(symbol) * 0.99, 2)
		self.order(symbol, 'market', 'gtc', 'immediate', price, quantity, 'buy')

if __name__ == '__main__':
	# rh = Robinhood('USER', 'PASS', 'ID')
	rh = Robinhood()
	rh.connect()
	rh.market_buy('SPY',1)
	rh.close()