import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bookmakers.helpers import *
# NB! Does not always find all odds. Caused by loading elements


def betsafe(sport='tennis'):

    web = 'https://www.betsafe.com/en/sport_labelsbook'
    firefox_path = '/usr/local/bin/'

    games = []
    odds = []
    path = '/home/per/Desktop/pythonProject/arbitrage_betting/' + sport + '/'
    filename = path + 'betsafe' + '_' + sport

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_path, options=options)
    driver.get(web)

    sport_labels_cn = 'ng-star-inserted'
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, sport_labels_cn)))
    sport_labels = driver.find_elements(By.CLASS_NAME, sport_labels_cn)

    for sport_label in sport_labels:
        if sport.lower() == sport_label.text.strip().lower():
            driver.execute_script('arguments[0].click();', sport_label)
            break

    # Collapse all dates
    try:
        collapsibles_css = "[class='obg-m-events-master-detail-header-toggle ico-chevron-right']"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, collapsibles_css)))
        collapsibles = driver.find_elements(By.CSS_SELECTOR, collapsibles_css)
        for collapsible in collapsibles:
            driver.execute_script('arguments[0].click();', collapsible)
    except selenium.common.exceptions.TimeoutException:
        print("Failed to find collapse button")

    # Show all (still hidden after collapse all)
    counter = 0
    try:
        show_all = "obg-show-more-less-button.ng-star-inserted"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, show_all)))
        show_buttons = driver.find_elements(By.CLASS_NAME, show_all)
        for show_button in show_buttons:
            show_text = ""
            while show_text[0:8].lower() != "show all" and counter < 1e2:
                counter += 1
                show_text = show_button.text.strip()
                driver.execute_script("arguments[0].click();", show_button)

    except selenium.common.exceptions.TimeoutException:
        print("Failed to find show all button")

    competition_css = "[class$='is-first obg-event-row-market ng-star-inserted']" # Not including handicap etc
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, competition_css)))
    competitions = driver.find_elements(By.CSS_SELECTOR, competition_css)

    for competition in competitions:
        events_css = 'ng-star-inserted'
        events = competition.find_elements(By.CLASS_NAME, events_css)

        for event in events:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", event)
                teams_cn = 'obg-selection.ng-star-inserted'
                teams = event.find_elements(By.CLASS_NAME, teams_cn)
                n_c = len(teams)
                names = [None]*n_c
                odds_event = [None]*n_c

                for i in range(n_c):
                    team = teams[i]
                    names[i] = team.find_element(By.CLASS_NAME, 'obg-selection-content-label-wrapper').text
                    odds_event[i] = team.find_element(By.CLASS_NAME, 'obg-numeric-change.ng-star-inserted').text
                    if all(odds_event) and odds_event:
                        games.append(game_string(*names))
                        odds.append(game_odds(*odds_event))

            except selenium.common.exceptions.NoSuchElementException:
                continue
            except IndexError:
                continue

        # Add competitions that were not found for the first search to end of list in loop
        if competition == competitions[-1]:
            driver.execute_script("arguments[0].scrollIntoView(true);", competition)
            competitions_update = driver.find_elements(By.CSS_SELECTOR, competition_css)
            if competitions_update[-1] != competitions[-1]:
                new_competitions = [c for c in competitions_update if c not in competitions]
                competitions.extend(new_competitions)
            else:
                break

    driver.close()
    save_frame(filename, games, odds)




