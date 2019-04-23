#
# Example strategy: SMA crossover
#
# If the 50 day SMA is greater than the 200 day SMA, hold the security (SPY)
# else, do not hold
#

import tradinglib.data as data
import tradinglib.robinhood as robinhood

def strategy(auth):
    """
    
    :param auth: Python dict
        'token' -> Robinhood auth token
        'refresh' -> Robinhood refresh token
        'account' -> Robinhood portfolio ID
    :return: None
    """
    prices = data.history("SPY", 200)
    sma50 = sum(prices[150:]) / 50
    sma200 = sum(prices) / 200

    # if greater, allocate 100% (1) of portfolio
    if sma50 > sma200:
        robinhood.allocate(auth, "SPY", 1)
    else:
        robinhood.allocate(auth, "SPY", 0)