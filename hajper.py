import time
# GETS REDIRECTED TO LIVE GAMES SOMETIMES HAVE TO FIX THIS
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from helpers import *


def hajper(sport='football'):
    web = "https://www.hajper.com/sv/sportsbook"
    firefox_path = "/usr/local/bin/"

    games = []
    odds = []
    n_odds = get_number_of_odds(sport)

    path = "/home/per/Desktop/pythonProject/arbitrage_betting/" + sport + "/"
    filename = path + "hajper" + "_" + sport

    # Open browser
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_path, options=options)
    driver.get(web)

    # Cookies
    cookie_cn = "btn.btn--ghost"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, cookie_cn)))
    cookie = driver.find_element(By.CLASS_NAME, cookie_cn)
    driver.execute_script("arguments[0].click();", cookie)

    # Switch frame to find matches
    iframe_tn = "iframe"
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, iframe_tn)))
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, iframe_tn))

    # Select sport
    sport_labels_cn = "sports-list-item-text-name"
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, sport_labels_cn)))
    sport_labels = driver.find_elements(By.CLASS_NAME, sport_labels_cn)
    for sport_label in sport_labels:
        if eng_to_swe(sport) == sport_label.text.strip().lower():  # Only match start of string
            driver.execute_script("arguments[0].click();", sport_label)
            break

    tabs_cn = "tab-switch-btn"
    "tabs-Center_TabSwitchResponsiveBlock_17974"
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, tabs_cn)))
    tabs = driver.find_elements(By.CLASS_NAME, tabs_cn)
    tabs_text = [tab.text for tab in tabs]
    counter = 0

    # Makes sure all league button is present
    while "Alla ligor" not in tabs_text and counter < 1e2:
        counter += 1
        tabs = driver.find_elements(By.CLASS_NAME, tabs_cn)
        tabs_text = [tab.text for tab in tabs]

    # Switch to find all leagues
    for tab in tabs:
        if tab.text.lower() == "alla ligor":
            driver.execute_script("arguments[0].click();", tab)

    # Show all leagues
    show_all_button_cn = "rj-league-list__show-all-btn"
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, show_all_button_cn)))
    show_all_button =  driver.find_element(By.CLASS_NAME, show_all_button_cn)
    driver.execute_script("arguments[0].click();", show_all_button)

    # Href strings live
    show_all_cn = "bet-inplay-btn-wrapper"
    # Store hrefs of competitions
    hrefs = set()  # Store links to scrape data
    competitions_cn = "rj-league-list__item-link"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, competitions_cn)))
    competitions = driver.find_elements(By.CLASS_NAME, competitions_cn)

    for competition in competitions:
        hrefs.add(competition.get_attribute("href"))

    events_cn = "rj-ev-list__ev-card__inner"
    names_cn = "rj-ev-list__bet-btn__content.rj-ev-list__bet-btn__text"
    odds_event_cn = "rj-ev-list__bet-btn__content.rj-ev-list__bet-btn__odd"

    for href in hrefs:
        if "https://m-se.hajper.com/sports/fotboll/spanien-copa-del-rey/" not in href:
            continue
        driver.get(href) # Open link to scrape
        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, events_cn)))
            events = driver.find_elements(By.CLASS_NAME, events_cn)
        except selenium.common.exceptions.TimeoutException:
            print("No events found")
            continue
        while events:
            event = events.pop(0)
            counter = 0

            # Retry until element it not stale.
            while counter < 10:
                try:
                    names_el = event.find_elements(By.CLASS_NAME, names_cn)
                    n_names = len(names_el)
                    names = [None] * n_names
                    for i in range(n_names):
                        names[i] = names_el[i].text
                    odds_event_el = event.find_elements(By.CLASS_NAME, odds_event_cn)
                    n_found_odds = len(odds_event_el)
                    odds_event = [None] * n_odds  # To find missing odds
                    for i in range(n_found_odds):
                        odds_event[i] = odds_event_el[i].text
                    break
                except selenium.common.exceptions.StaleElementReferenceException:
                    print("STALE BABY")
                    WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, events_cn)))
                    events = driver.find_elements(By.CLASS_NAME, events_cn)
                    event = events.pop(0)
                    counter += 1

            # Need to check if empty odds (have not done this for hajper yet)

            if all(odds_event) and odds_event:
                games.append(game_string(*names))
                odds.append(game_odds(*odds_event))
                print(href)
                print(game_string(*names), game_odds(*odds_event))

            if not events:
                driver.execute_script("arguments[0].scrollIntoView(true);", event)  # Scroll to find all
                time.sleep(1)
                events = driver.find_elements(By.CLASS_NAME, events_cn)  # Find new dynamic elements
                if event in events:
                    slice_index = events.index(event)
                    events = events[slice_index + 1:]  # Slicing to prevent duplicates


    driver.close()
    save_frame(filename, games, odds, web)
