from pathlib import Path
from selenium import webdriver
from bs4 import BeautifulSoup

def ScrapeWords(words, main_url, first_page):
    driver = webdriver.Chrome()
    next_page = first_page

    for _ in range(2):
        # access the website
        driver.get(f"{main_url}/{next_page}")
        all_content = driver.page_source

        # parse html with BeautifulSoup
        soup = BeautifulSoup(all_content)

        # find main content (class: TCont)
        content = soup.find_all('div', attrs={'class': 'TCont'})

        # find list of words
        list = content[0].find_all('li')
        for li in list:
            anchor = li.find('a')
            if not anchor: 
                continue
            word = anchor.string
            words.append(word)

        # find next page link (only displays 500 words at once)
        next_page = content[0].find('div', attrs={'class': 'nextLink'}).find_next()['href']
   

def SaveWordsToFile(words, word_file):
    # create Path object with path of word_file
    word_file = Path(word_file)

    # delete word_file if already exist
    word_file.unlink(missing_ok=True)

    # open file and write words
    f = open(word_file, 'a')
    for word in words:
        f.write(word + '\n')

    f.close()


if __name__ == '__main__':
    # list of words
    words = []

    main_url = 'https://www.thefreedictionary.com/'
    next_page = '5-letter-words.htm'

    ScrapeWords(words, main_url, next_page)
    SaveWordsToFile(words, "words.txt")
    print(words)