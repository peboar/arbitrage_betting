from helpers import *
import json
import pickle

sport = "football"
webb = "bethard"

path = "/home/per/Desktop/pythonProject/arbitrage_betting/" + sport + "/"
filename = path + webb + "_" + sport

with open("/home/per/Desktop/pythonProject/arbitrage_betting/temp.txt", 'r') as file:
    lines = file.readlines()
    events = []
    odds = []
    for line in lines:  
        temp = line.split("[")
        events.append(simple_name(temp[0]))
        odds.append(json.loads("["+temp[1]))


# save_frame(filename, events, odds)

read_test = pickle.load(open(filename, 'rb'))

print(read_test)
