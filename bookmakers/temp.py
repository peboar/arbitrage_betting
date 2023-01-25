from bookmakers.helpers import *

sport = "football"
import json

with open("top_leagues.json") as json_file:
    data = json.load(json_file)
    leagues = data[sport]


with open("temp.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        if len(line.split("-")) > 1:
            if any(l.lower() in line.lower() and eng_to_swe(c.lower()) in line.lower() for c, l in leagues):
                print(line)
        else:
            if any(l.lower() in line.lower() for c, l in leagues):
                print(line)
        # for country, league in leagues:


            # print(fuzz.ratio(line, league))

