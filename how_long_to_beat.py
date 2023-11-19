# First we need to get which games you have in xml format
import urllib.request           # For getting HTML from the site
from bs4 import BeautifulSoup   # For handling html easier
from howlongtobeatpy import HowLongToBeat   # For gametimes

def get_game_dic(): # Gets username requests xml of games and create a list with name of the games
    username = input("What is your steam user name? ").lower()

    url = f'https://steamcommunity.com/id/{username}/games/?tab=all&xml=1'

    # In the following url we can see all the games in xml format
    # We need following parts for every game so lets get them
    # <game>
    #   <appID>1406180</appID>
    # <name>
    #   <![CDATA[ Fantasy Grounds Unity Demo ]]>
    # </name>

    data = urllib.request.urlopen(url)          # Get xml
    soup = BeautifulSoup(data, features="xml")  # Parse xml using beatifulsoup  

    game_xml_list = soup.find_all("game")       # Get all game parts and create a list

    final_list = []
    for i in game_xml_list:                     # Loop through list to get each game's name and store into list
        final_list.append(i.find('name').text)

    return final_list

def order_by_playtime(game_list):  # Collect data for each game from HowLongToBeat.com take ordering preferences as input and return the output
    game_time_list = []
    for i in game_list:
        results = HowLongToBeat().search(i)
        if results is not None and len(results) > 0:
            best_element = max(results, key=lambda element: element.similarity)
            game_time_list.append({"name":best_element.game_name, "main_story": int(best_element.main_story), "main_extra": int(best_element.main_extra), "completionist": int(best_element.completionist), "all_styles": int(best_element.all_styles)})
    while True:
        try:
            choice = int(input("Based on what shoul it be ordered?\nType 1 for main story\nType 2 for main story + extras\nType 3 for completionist\nType 4 for all styles\n"))
            if choice in range(1, 5):
                while True:
                    choice2 = int(input("Type 1 for increasing order\nType 2 for decreasing order\n"))
                    if choice2 not in range(1,3):
                        print("Please choose an integer between 1-2!")
                        continue
                    else:
                        break
                decreasing = True if choice2 == 2 else False
                if choice == 1:
                    game_time_list_sorted = sorted(game_time_list, key=lambda x: x["main_story"], reverse=decreasing)
                if choice == 2:
                    game_time_list_sorted = sorted(game_time_list, key=lambda x: x["main_extra"], reverse=decreasing)
                if choice == 3:
                    game_time_list_sorted = sorted(game_time_list, key=lambda x: x["completionist"], reverse=decreasing)
                if choice == 4:
                    game_time_list_sorted = sorted(game_time_list, key=lambda x: x["all_styles"], reverse=decreasing)
                return game_time_list_sorted
            else:
                print("Please choose an integer between 1-2-3-4!")
                continue
        except ValueError:
            print("Not an integer!")
            continue

listed = order_by_playtime(get_game_dic())
for i in listed:
    print(i)

