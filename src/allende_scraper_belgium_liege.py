# allende-scraper-belgium_liege.py
# Main repo: https://github.com/GoGroGlo/a-place-for-salvador-allende
# Liège-specific scraper covering only this list: http://www.abacq.org/calle/index.php?2013/10/05/618-provincia-de-liege-belgica



# ------------------------------------------------------ #



### IMPORTS ###


# web scraping tutorial courtesy of https://www.educative.io/blog/python-web-scraping-tutorial


from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller as chromedriver
import re
import pandas as pd 


# local import - I hope this works
import allende_scraper_main as asm



# ------------------------------------------------------ #



# create a dictionary of lists that's easily translatable into our existing db
data = {
    'id'                         : [],
    'name'                       : [],
    'type'                       : [],
    'region'                     : [],
    'country'                    : [],
    'locale_1'                   : [],
    'locale_2'                   : [],
    'locale_3'                   : [],
    'locale_4'                   : [],
    'locale_5'                   : [],
    'zip_code'                   : [],
    'latitude'                   : [],
    'longitude'                  : [],
    'oldest_known_year'          : [],
    'oldest_known_month'         : [],
    'oldest_known_day'           : [],
    'oldest_known_source'        : [],
    'desc'                       : [],
    'desc_language'              : [],
    'alt_name'                   : [],
    'former_name'                : [],
    'verified_in_maps'           : [],
    'openstreetmap_link'         : [],
    'google_maps_link'           : [],
    'abacq_reference'            : [],
}


# create a Google Chrome driver object
# https://stackoverflow.com/questions/69918148/deprecationwarning-executable-path-has-been-deprecated-please-pass-in-a-servic
# s = Service('C:\\Users\\canogle\\.cache\\selenium\\chromedriver\\win32\\110.0.5481.77\\chromedriver.exe')
# selenium.common.exceptions.SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 110
# Current browser version is 112.0.5615.49 with binary path C: \Program Files\Google\Chrome\Application\chrome.exe
s = Service(chromedriver.install())
driver = webdriver.Chrome(service=s)


# our base link
link = 'http://www.abacq.org/calle/index.php?2013/10/05/618-provincia-de-liege-belgica'


# default country
country_en = 'Belgium'


# fetch base link and extract only the relevant part of it
driver.get(link)
article_soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=SoupStrainer("div", class_="post"))
asm.humanizer(asm.timer)
text = article_soup.get_text()
lower_text = text.lower()
print(text)


#
# get all LOCALE_1
#
locale_1_soup = article_soup.find_all("strong")
locale_1_soup = list(locale_1_soup)
locale_1_list = []
for locale_1 in locale_1_soup:
    locale_1 = str(locale_1)
    locale_1 = re.search(r'<strong>(.*)<\/strong>', locale_1)
    locale_1 = str(locale_1.group(1))
    locale_1_list.append(locale_1)


#
# for each LOCALE_1, give them the same base information as the rest of the article
#
for (i, locale_1) in enumerate(locale_1_list, start=1):

    print(f'\n\n>>> Parsing locale {str(i)} of {str(len(locale_1_list))}: {locale_1}')

    #
    # get ID (null)
    #
    id = ''
    data['id'].append(id)
    print(f'ID: {id}')

    #
    # get COUNTRY and REGION
    #
    asm.get_country_and_region(link, data)

    #
    # cross-check LOCALE_1 with OSM
    #
    asm.osm_check(locale_1, data)

    #
    # extract OSM info if any
    #
    asm.extract_osm_info(data)

    #
    # get NAME
    #
    asm.get_name(article_soup, data)

    #
    # get TYPE
    #
    asm.get_type(data)

    #
    # get DESC
    # whatever text is in the memorial place
    # had to move this before get_oldest_known_source so that the function can use desc_soup
    #
    desc = ''
    global desc_soup
    desc_soup = article_soup.find_all("em")
    desc_soup = list(desc_soup)
    for desc_item in desc_soup:
        desc_item = str(desc_item)
        desc_item = desc_item.strip('</em>')
        desc += desc_item + '\n'
    desc = desc.replace('<br/>', '')
    data['desc'].append(desc)
    print(f'Desc: {desc}')

    #
    # get DESC_LANGUAGE (null)
    # won't assume anything here for now because most of the descriptions I see are in Spanish, regardless of the region
    #
    desc_language = ''
    data['desc_language'].append(desc_language)
    print(f'Desc language: {desc_language}')

    #
    # get OLDEST_KNOWN_YEAR
    #
    asm.get_oldest_known_year(link, text, data)

    #
    # get OLDEST_KNOWN_MONTH
    #
    asm.get_oldest_known_month(link, lower_text, data)

    #
    # get OLDEST_KNOWN_DAY
    #
    asm.get_oldest_known_day(link, lower_text, data)

    #
    # get OLDEST_KNOWN_SOURCE
    #
    asm.get_oldest_known_source(desc, data)

    #
    # get ALT_NAME (null)
    #
    alt_name = ''
    data['alt_name'].append(alt_name)
    print(f'Alt name: {alt_name}')

    # 
    # get FORMER_NAME (null)
    #
    former_name = ''
    data['former_name'].append(former_name)
    print(f'Former name: {former_name}')

    #
    # get VERIFIED_IN_MAPS and OPENSTREETMAP_LINK
    #
    asm.get_verified_in_maps_and_osm_link(data)

    #
    # get GOOGLE_MAPS_LINK (null)
    #
    google_maps_link = ''
    data['google_maps_link'].append(google_maps_link)
    print(f'Google Maps link: {google_maps_link}')

    #
    # get ABACQ_REFERENCE
    # basically the url we're working with
    #
    data['abacq_reference'].append(link)

    #
    # stay in the web page like a normal human would
    #
    asm.humanizer(asm.timer)

    #
    # clear browser cache for the next iteration
    #
    asm.clear_cache()



# ------------------------------------------------------ #



### 4. EXPORT THE DATA ###


# create a dataframe of all info collected
data_df = pd.DataFrame(data=data)
print('\nDataFrame created:\n')
print(data_df)

# export dataframe - xlsx supports unicode, so no more encoding fiascos compared to saving to csv
# data_df.to_excel(f'{country_en}.xlsx', index=False) # for test files
data_df.to_excel(f'countries/{country_en}.xlsx', index=False) # for main files
print(f'DataFrame saved in \'countries/{country_en}.xlsx\'.')



# ------------------------------------------------------ #


