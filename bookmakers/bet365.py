from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bookmakers.helpers import *

from selenium.webdriver.chrome.options import Options



def bet365(sport='tennis'):
    web = 'https://www.bet365.com'
def bet365(sport='tennis'):
    web = 'https://www.bet365.com'
    browser_path = '/usr/local/bin/'

    games = []
    browser_path = '/usr/local/bin/'

    games = []
    odds = []
    path = '/home/per/Desktop/pythonProject/arbitrage_betting/' + sport + '/'
    filename = path + 'comeon' + '_' + sport

    # Open browser
    # options = Options()
    # options.add_argument('--headless')
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.get(web)

    sport_labels_cn = 'wn-PreMatchItem'
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, sport_labels_cn)))
    sport_labels_cn = driver.find_elements(By.CLASS_NAME, sport_labels_cn)

    for sport_label in sport_labels_cn:
        if eng_to_swe(sport) == sport_label.text.strip().lower():
            driver.execute_script('arguments[0].click();', sport_label)
            break

    all_matches_cs = '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[3]/div[2]/div/div/div[2]/div[1]/span'
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, all_matches_cs)))
    full_list = driver.find_element_by_xpath(all_matches_cs)
    driver.execute_script('arguments[0].click();', full_list)

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'src-CompetitionMarketGroup')))
    competitions = driver.find_elements(By.CLASS_NAME, 'src-CompetitionMarketGroup')

    for i in range(len(competitions)):

        names = competitions[i].find_elements(By.CLASS_NAME, 'rcl-ParticipantFixtureDetailsTeam')
        odds = competitions[i].find_elements(By.CLASS_NAME, 'sgl-ParticipantOddsOnly80_Odds')
        n = len(odds)//2
        odds1 = odds[:n]
        odds2 = odds[n:]

        #Has to wait to get all matches for some reason
        if i == 0:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'rcl-ParticipantFixtureDetailsTeam')))

        for j in range(n):
            print([i.text for i in names])
            if odds[j].text.strip():
                if '/' in names[2*j].text and '/' in names[2*j+1].text:
                    n1 = names[2*j].text.strip().lower()
                    n2 = names[2*j+1].text.strip().lower()
                else:
                    n1 = names[2*j].text.strip().lower().split()[0] + ' ' + names[2*j].text.strip().lower().split()[-1]
                    n2 = names[2*j+1].text.strip().lower().split()[0] + ' ' + names[2*j+1].text.strip().lower().split()[-1]
                match = n1 + ' vs ' + n2
                match = match.replace('-', ' ')
                o1 = float(odds1[j].text.strip())
                o2 = float(odds2[j].text.strip())
                # matches.append(unidecode(match), Odds([o1, o2], web))







