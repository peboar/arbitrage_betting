import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bookmakers.helpers import *


def sport888(sport="football"):
    web = "https://www.888sport.se/"
    firefox_path = "/usr/local/bin/"

    games = []
    odds = []

    path = "/home/per/Desktop/pythonProject/arbitrage_betting/" + sport + "/"
    filename = path + "888sport" + "_" + sport

    # Open browser
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_path, options=options)
    driver.get(web)

    # Cookies
    cookie_id = "onetrust-accept-btn-handler"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, cookie_id)))
    cookie = driver.find_element(By.ID, cookie_id)
    driver.execute_script("arguments[0].click();", cookie)

    # Collapse sport menu
    collapse_menu_cn = "menu-arrow"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, collapse_menu_cn)))
    collapse_menu = driver.find_element(By.CLASS_NAME, collapse_menu_cn)
    driver.execute_script("arguments[0].click();", collapse_menu)

    # Sport menu class
    menu_cn = "popularMenu.showDrawer.do-not-close-null"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, menu_cn)))
    menu = driver.find_element(By.CLASS_NAME, menu_cn)

    # Select sport
    sport_labels_cn = "ellipsis-span"
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, sport_labels_cn)))
    sport_labels = menu.find_elements(By.CLASS_NAME, sport_labels_cn)

    for sport_label in sport_labels:
        if eng_to_swe(sport.lower()) == sport_label.text.strip().lower():
            driver.execute_script('arguments[0].click();', sport_label)
            break

    # Tab to find all competitions
    tabs_css = "a[class^='pocTabs__tab']"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, tabs_css)))
    tabs = driver.find_elements(By.CSS_SELECTOR, tabs_css)

    # Href strings live
    show_all_cn = "bet-inplay-btn-wrapper"
    hrefs = []  # Store links to scrape data
    href_tn = "a"

    # Href string all competitions
    leagues_cn = "bb-content-section.bb_generic_sport_competitions__item"
    collapsibles_cn = "bb-icon.bb-icon--orange-dropdown.bb-icon-" \
                      "-width-12.bb-content-section__dropdown-icon.bb-icon--rotate-180"

    for i in range(len(tabs)):
        tab = tabs[i]
        # Store href of live matches
        if i == 0:  # Have to use index here since strings are not the same for different sports
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, show_all_cn)))
                show_button = driver.find_element(By.CLASS_NAME, show_all_cn)
                href_live_tag = show_button.find_element(By.TAG_NAME, href_tn)
                hrefs.append(href_live_tag.get_attribute("href"))
            except selenium.common.exceptions.NoSuchElementException:
                print("Failed to find live matches")

        # Store href of all competitions
        if tab.text.strip().lower() == "tävlingar":
            driver.execute_script('arguments[0].click();', tab)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, collapsibles_cn)))
            collapsibles = driver.find_elements(By.CLASS_NAME, collapsibles_cn)

            # Collapse all hidden
            for collapsible in collapsibles:
                driver.execute_script('arguments[0].click();', collapsible)

            # Save links to competitions
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, leagues_cn)))
            leagues = driver.find_elements(By.CLASS_NAME, leagues_cn)

            for league in leagues:
                href_league_tags = league.find_elements(By.TAG_NAME, href_tn)
                hrefs.extend([href.get_attribute("href") for href in href_league_tags])

    # Scraping odds from different links
    # Different class names for the live link and the competitions links
    events_cn_list = ["bb-sport-event", "sport-event.media-cells.preplay-event-selections"]
    names_css_list = ["span[class='bb-sport-event__detail-name']", "div[class^='competitor competitor']"]
    odds_event_css_list = ["span[class^='bb-sport-event__selection bb-']", "div[class='preplay-bet-button']"]

    for href in hrefs:
        if "livejustnu" in href:
            events_cn = events_cn_list[0]
            names_css = names_css_list[0]
            odds_event_css = odds_event_css_list[0]
        else:
            events_cn = events_cn_list[1]
            names_css = names_css_list[1]
            odds_event_css = odds_event_css_list[1]

        driver.get(href) # Open link to scrape
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, events_cn)))
            events = driver.find_elements(By.CLASS_NAME, events_cn)
        except selenium.common.exceptions.TimeoutException:
            print("No events found")
            continue

        for event in events:
            names_el = event.find_elements(By.CSS_SELECTOR, names_css)
            n_names = len(names_el)
            names = [None] * n_names
            for i in range(n_names):
                names[i] = names_el[i].text

            odds_event_el = event.find_elements(By.CSS_SELECTOR, odds_event_css)

            n_odds = len(odds_event_el)
            odds_event = [None] * n_odds  # Have to use n_odds for check if odds are missing
            for i in range(n_odds):
                if odds_event_el[i].text != "0.00":  # Empty odds sometimes given as zeroes
                    odds_event[i] = odds_event_el[i].text

            if all(odds_event) and odds_event:
                games.append(game_string(*names))
                odds.append(game_odds(*odds_event))

    driver.close()
    save_frame(filename, games, odds)
