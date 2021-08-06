import urllib.request
import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
websites = {'action_network_baseball' : 'https://www.actionnetwork.com/mlb/odds'}

#regex that pulls only uppercase letters from string
uppercase = '[A-Z]+'

#function that returns books and odds in structured format
def mlb_get_content(html):
    content = []
    book_list = []
    team_list = []
    opening_odds_list = []
    book_odds_list = []
    soup = BeautifulSoup(html, 'lxml')
    book_html = soup.find_all('div', attrs= { 'class': 'compare-odds-book-header-cell__logo'})
    for book in book_html:
        book_list.append(book.find('img')['alt'])
    team_html = soup.find_all('div', attrs = { 'class': 'game-info__team'})
    for team in team_html:
        team_string = (team.getText())
        match = re.findall(uppercase, team_string[-3:])
        team_list.append(match[0])
    opening_odds_html = soup.find_all('div', attrs = { 'class': 'best-odds__open-cell'})
    for odd in opening_odds_html:
        opening_odds_list.append(odd.getText())
    book_odds_html = soup.find_all('div', attrs = {'class': 'book-cell__odds'})
    for odd in book_odds_html:
        book_odds_list.append(odd.getText())
    #print output
    print(book_list)
    print(team_list)
    print(opening_odds_list)
    print(book_odds_list)
    if (len(team_list) > len(opening_odds_list)):
        middle_index = len(team_list)//2
        team_list = team_list[0:middle_index]

    print(len(team_list))
    print(len(opening_odds_list))
    print(len(book_odds_list))
    team_dict = {}
    i = 0
    for team in team_list:
        odds_dict = {}
        print(i)
        odds_dict['opening'] = opening_odds_list[i]
        odds_dict['best'] = book_odds_list[i]
        i+=1
        team_dict[team] = odds_dict
    print(team_dict)
    print(len(team_dict))
    df = pd.DataFrame.from_dict(team_dict)
    print(df)

def test_function(html):
    soup = BeautifulSoup(html, 'lxml')
    opening_odds_html = soup.find_all('tr')
    




#function to scrape all mlb odds from action network
def mlb():
    driver = webdriver.Chrome('/Users/JakeLawson/Desktop/arb/chromedriver')
    driver.get(websites['action_network_baseball'])
    time.sleep(10)
    html = driver.page_source
    mlb_get_content(html)
mlb()

#<div class="compare-odds-book-header-cell__logo"><img class="" height="21" alt="DraftKings" src="https://assets.actionnetwork.com/477013_DraftKings@1x.png"></div>
#<div class="best-odds__open-cell">+110</div>
#soup.find("meta", {"name":"City"})['content']
#<div class="book-cell__odds"><span class="custom-1qynun2 ewbmh0c1"><span class=" custom-wkctv e7ufv0u0" color="nothing"><svg viewBox="0 0 24 24" width="40" height="40" xmlns="https://www.w3.org/2000/svg" class="highlight-text__arrow highlight-text__arrow--placeholder custom-inrq evhdyr10" fill="#00C358" stroke="#00C358" stroke-width="0"><title></title><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"></path></svg><span class="highlight-text__children">+106</span></span></span><span class="book-cell__secondary"><span class=" custom-amkfwb e7ufv0u0" color="nothing"><span class="highlight-text__children">ML</span></span></span></div>
