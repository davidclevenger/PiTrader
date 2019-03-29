# on each iteration of server thread code do:
#
#   check for new instructions from client
#       if got new data, update strategies/metadata
#
#   get stock data from AlphaVantage
#   
#   process stock data with strategies to determine buy/sell orders
#   
#   invoke Robinhood API to execute trades
#   
#   return data to client (JSON Export)
#   
#   log data
#
# end

