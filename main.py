import sys
sys.path.insert(0, r"C:\Users\ogy572\PycharmProjects\arbitrage_betting\bookmakers")


import json

from bookmakers import *


sport = "football"
with open("top_leagues.json") as json_file:
    data = json.load(json_file)
    leagues = data[sport]


# matches = Matches()
# print("hajper")
# hajper()
# print("888sport")
# sport888()

print("bethard")
bethard("football", leagues)
#
# # print("snabbare")
# snabbare("football")

# print("betsafe")
# betsafe('football')

# print("comeon")
# comeon()

# print('leovegas')
# leovegas()

# print('unibet')
# unibet()

# print('redbet')
# redbet()



# print('bet365')
# bet365()







# print(matches)
# matches.get_surebets()
# matches.print_surebets()
