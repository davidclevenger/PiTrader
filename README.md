# PiTrader
Senior Design Project Repo


## Client -> Server
1. Username
2. Authorization Token 
3. Refresh token
4. Code (strategy)

## Server side sanitizing
1. find 'def strategy(context):' in file uploaded
2. check if import exists in function
2a. if imports exist, reject
2b. if not, put strategy in a directory with username

## Server File Hierarchy

/-users
  |-Dave
  |-Guru
  |-Parker
    |-strategy.py
    |-metrics.txt
  ...
  |-Zorro
/-server
  |-harness.py (code used to run strategies)
  |-server.py (code used to accept uploads and drive strategy harness)
