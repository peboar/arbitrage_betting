from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from helpers import *


def leovegas(sport='tennis'):
    games = []
    odds = []

    web = "https://www.leovegas.com/sv-se/betting#home"
    firefox_path = "/usr/local/bin/"
    path = '/home/per/Desktop/pythonProject/arbitrage_betting/' + sport + '/'
    filename = path + 'leovegas' + '_' + sport

    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_path, options=options)
    driver.get(web)

    # Cookies
    cookie_cn = 'wNEmG.hjN2x.TGik8.XFlfq'
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, cookie_cn)))
    cookie = driver.find_element(By.CLASS_NAME, cookie_cn)
    driver.execute_script("arguments[0].click();", cookie)

    # Needs to scroll
    driver.execute_script("window.scrollTo(0, 100)")

    column_cn = 'ColumnContentSelector__contentOption___N7TMS'
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, column_cn)))
    columns = driver.find_elements(By.CLASS_NAME, column_cn)

    column_buttons_cn = 'Button__btn___3zXcJ'
    column_buttons = [column.find_element(By.CLASS_NAME, column_buttons_cn) for column in columns]
    column_buttons = column_buttons[0:2]

    # Loop to get both live and coming games
    for button in column_buttons:
        # Switch between live and coming games
        driver.execute_script("arguments[0].click();", button)

        sport_labels_cn = 'SportsTabs__sportsTab___3XoY9'
        sport_labels = driver.find_elements(By.CLASS_NAME, sport_labels_cn)
        for sport_label in sport_labels:
            if eng_to_swe(sport) == sport_label.text.strip().lower():
                driver.execute_script("arguments[0].click();", sport_label)
                break

        collapsibles_cn = 'ListPage__accordionWrapper___2HUoy.Accordion__accordion___1xJEC.Accordion__collapsed___1Kddw'
        click_collapsible_cn = 'ListPage__accordionHeader___3qXgs.Accordion__header___1BfIp' # Need this to drop down

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, collapsibles_cn)))
            collapsibles = driver.find_elements(By.CLASS_NAME, collapsibles_cn)
            for collapsible in collapsibles:
                driver.execute_script('arguments[0].scrollIntoView(true);', collapsible)
                click_collapsible = collapsible.find_element(By.CLASS_NAME, click_collapsible_cn) # Collapse
                driver.execute_script("arguments[0].click();", click_collapsible)

        except selenium.common.exceptions.TimeoutException:
            print("Collapsible not found")

        # Scraping odds
        try:
            events_cn = 'Card__card___2lW42.Card__clickable___4GOzb.Card__generic___2TYEB'
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, events_cn)))
            events = driver.find_elements(By.CLASS_NAME, events_cn)
            names_cs_cn = 'Card__teamNames___2Fmd1'
            odds_event_cn = 'Card__offerWrapper___yhmWO'
            for event in events:
                names = event.find_element(By.CLASS_NAME, names_cs_cn).text
                odds_event = event.find_element(By.CLASS_NAME, odds_event_cn).text
                if odds_event and names:
                    games.append(game_string(names)) # Single string only
                    odds.append(game_odds(*odds_event.split()))
        except selenium.common.exceptions.TimeoutException:
            print("Games not found")

    driver.close()
    save_frame(filename, games, odds)