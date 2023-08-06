# allende-scraper-france-links.py
# Main repo: https://github.com/GoGroGlo/a-place-for-salvador-allende

# Automates the data collection by verifying using https://www.openstreetmap.org
# the list of links that weren't already captured in allende_scraper_france_streets.py via 
# http://www.abacq.org/calle/index.php?2009/05/13/349-salvador-allende-en-francia 


# ------------------------------------------------------ #


### IMPORTS ###


# web scraping tutorial courtesy of 
# https://www.educative.io/blog/python-web-scraping-tutorial

# standard library imports
import re
import math

# third party imports
import pandas as pd 
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

# local import
import allende_scraper_main as asm


# ------------------------------------------------------ #


### CONSTANTS ###


country_en = 'France'
region = 'Europe'


# how long (in seconds) would you like sleep timers to 
# wait before continuing with the scraping?
timer = 30


# URLs
links_exceptions = [
                    'http://www.abacq.org/calle/index.php?2009/05/13/349-salvador-allende-en-francia', 
                    'http://www.abacq.org/calle/index.php?2007/02/18/2-francia-le-blanc-mesnil', 
                    'http://www.abacq.org/calle/index.php?2009/12/08/445-victor-jara-francia', 
                    'http://www.abacq.org/calle/index.php?2007/02/18/56-pablo-neruda-en-francia', 
                    'http://www.abacq.org/calle/index.php?2007/02/18/22-victor-jara',
                    'http://www.abacq.org/calle/index.php?2007/03/09/49-la-region-parisina-francia',
                    'http://www.abacq.org/calle/index.php?2007/03/13/54-en-la-reunion-oceano-indico-francia',
]


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


# ------------------------------------------------------ #


### MAIN ###

### PREPARE LISTS ###


# placeholder list of links to be scraped
# the 18 is because there are 17 sets from allende_scraper_france_streets.py
# and this is basically the next set
allende_in_france_links_18 = []


# allende_in_france_links_in_locales.txt is the list of links
# that were already caught in allende_scraper_france_streets.py.
# we'll remove these links from allende_in_france_links.txt
# and whatever remains gets stored in the allende_in_france_links_18 list
with open('france\\allende_in_france_links.txt','r') as f:
    for l in f.readlines():
        l = l.strip()
        with open('france\\allende_in_france_links_in_locales.txt','r') as g:
            if l not in g.readlines():
                allende_in_france_links_18.append(l)


# now, some of the links in allende_in_france_links_in_locales.txt
# refer to a locale that has more than one corresponding link.
# we'll remove from allende_in_france_links_18 those links
# whose locale is already included in allende_in_france_links_in_locales.txt

# placeholder list for locales
locales_in_url = []

with open('france\\allende_in_france_links_in_locales.txt','r') as g:
    for m in g.readlines():
        m = m.strip()
		# extract the locale name from the link
        m_locale = re.search(r'\d{4}\/\d{2}\/\d{2}\/\d*((?:-\w*)*)-francia', m)
        m_locale = m_locale.group(1)
        # then add the locale to the placeholder list
        locales_in_url.append(m_locale)

# then remove the link from allende_in_france_links_18
# if it matches a locale we've already collected
for locale in locales_in_url:
    for link in allende_in_france_links_18:
        if str(locale) in str(link):
            allende_in_france_links_18.remove(link)


# remove exceptions from allende_in_france_links_18
for link in links_exceptions:
     if link in allende_in_france_links_18:
         allende_in_france_links_18.remove(link)

for i in ['victor-jara', 'pablo-neruda']:
    for link in allende_in_france_links_18:
        if i in str(link):
            allende_in_france_links_18.remove(link)


# save the final allende_in_france_links_18 in a file
with open('france\\allende_in_france_links_18.txt','w') as h:
	for l in allende_in_france_links_18:
		h.write(f'{l}\n')
# print for logging purposes
print('allende_in_france_links_18.txt created.')


# ------------------------------------------------------ #


### SPLIT LOCALE LIST INTO CHUNKS ###


# allende_in_france_links_18.txt says there are 93 links
# I did 3 sets of 31 each
# we'll just copy the chunks generator from allende_scraper_main.py

# let user decide how many links each chunk should have
try:
    chunk_number = int(input(
        '>>> Separate single-locale list into chunks with x links each? Enter number if yes, press Enter if no: '))
except:
    chunk_number = None

if chunk_number is not None:
    # we have to take note of which chunks we've done 
    # so that we don't repeat work
    try:
        target_chunk = int(input(
            f'>>> {math.ceil(len(allende_in_france_links_18) / chunk_number)} chunks generated - Enter the number of the chunk you want to work on: '))
    # typo prevention
    except:
        target_chunk = int(input(
            f'>>> Try again - {math.ceil(len(allende_in_france_links_18) / chunk_number)} chunks generated - Enter the number of the chunk you want to work on: '))
    while target_chunk > math.ceil(len(allende_in_france_links_18) / chunk_number):
        target_chunk = int(input(
            f'>>> Try again - {math.ceil(len(allende_in_france_links_18) / chunk_number)} chunks generated - Enter the number of the chunk you want to work on: '))

    links_for_checking = asm.chunks(allende_in_france_links_18, chunk_number)
    # skip through chunks that we don't need
    _i = 1
    while _i < target_chunk:
        next(links_for_checking)
        _i += 1
    # this next iteration is the chunk we want to work with
    links_for_checking = next(links_for_checking)


# ------------------------------------------------------ #


### WORK WITH EACH LINK ###


# start the browser
try:
    asm.create_driver()

    # every link is basically an article 
    # so we'll retrieve their contents
    for (i, link) in enumerate(links_for_checking, start=1):
        asm.browser_window(link)


        # we are only interested in the article itself, 
        # not the comments, sidebar, etc.
        article_soup = BeautifulSoup(asm.driver.page_source, 'html.parser', parse_only=SoupStrainer(
            "div", class_="post"))  
        # , from_encoding='windows-1252', exclude_encodings=['unicode', 'utf-8'])

        
        # stay in the web page like a normal human would
        asm.humanizer(timer)

        
        # then go on with our automated lives
        print(
            f'\n>>> Parsing single-locale article {str(i)} of {str(len(links_for_checking))}: {link}...\n')
        text = article_soup.get_text()
        lower_text = text.lower()
        print(text)

        
        # get ID (null)
        id = ''
        data['id'].append(id)
        print(f'ID: {id}')

        
        # get COUNTRY and REGION
        asm.get_country_and_region(link, data)

        
        # get LOCALE_1
        # we'll take the locale found in abacq as the default locale_1
        locale_1 = article_soup.find("strong")
        locale_1 = str(locale_1)
        locale_1 = re.search(r'<strong>(.*)<\/strong>', locale_1)
        try:
            str(locale_1.group(1))
        except:
            locale_1 = article_soup.find("h2", class_="post-title")
            locale_1 = str(locale_1)
            locale_1 = re.search(
                r'<h2 class="post-title">(.*)(?:\.|,)\s*.*<\/h2>', locale_1)
            locale_1 = str(locale_1.group(1))
        else:
            locale_1 = str(locale_1.group(1))
        
        # when we have this abacq locale, 
        # we then cross-check this with OpenStreetMap
        asm.osm_check(locale_1, data)

        
        # extract OSM info if any
        asm.extract_osm_info(data)

        
        # get NAME
        asm.get_name(article_soup, data)

        
        # get TYPE
        asm.get_type(asm.osm_info, asm.name, data)

        
        # get DESC
        # whatever text is in the memorial place.
        # had to move this before get_oldest_known_source 
        # so that the function can use desc_soup
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

        
        # get DESC_LANGUAGE (null)
        # won't assume anything here for now because 
        # most of the descriptions I see are in Spanish, regardless of the region
        desc_language = ''
        data['desc_language'].append(desc_language)
        print(f'Desc language: {desc_language}')

        
        # get OLDEST_KNOWN_YEAR
        asm.get_oldest_known_year(link, text, data)

        
        # get OLDEST_KNOWN_MONTH
        asm.get_oldest_known_month(link, lower_text, data)

        
        # get OLDEST_KNOWN_DAY
        asm.get_oldest_known_day(link, lower_text, data)

        
        # get OLDEST_KNOWN_SOURCE
        asm.get_oldest_known_source(desc, data)

        
        # get ALT_NAME (null)
        alt_name = ''
        data['alt_name'].append(alt_name)
        print(f'Alt name: {alt_name}')

        
        # get FORMER_NAME (null)
        former_name = ''
        data['former_name'].append(former_name)
        print(f'Former name: {former_name}')

        
        # get VERIFIED_IN_MAPS and OPENSTREETMAP_LINK
        asm.get_verified_in_maps_and_osm_link(asm.osm_info, data)

        
        # get GOOGLE_MAPS_LINK (null)
        google_maps_link = ''
        data['google_maps_link'].append(google_maps_link)
        print(f'Google Maps link: {google_maps_link}')

        
        # get ABACQ_REFERENCE
        # basically the url we're working with
        data['abacq_reference'].append(link)

        
        # stay in the web page like a normal human would
        asm.humanizer(timer)

# quit the browser properly regardless of whether it returns an exception
finally:
    asm.driver.quit()


# ------------------------------------------------------ #


### EXPORT THE DATA ###


# create a dataframe of all info collected
data_df = pd.DataFrame(data=data)
print('\nDataFrame created:\n')
print(data_df)


# export dataframe - xlsx supports unicode, 
# so no more encoding fiascos compared to saving to csv
# data_df.to_excel(
#     f'test_files/{country_en}_{target_chunk+17}.xlsx', index=False) # for test files
data_df.to_excel(
    f'countries/{country_en}_{target_chunk+17}.xlsx', index=False) # for main files
print(
    f'DataFrame saved in \'countries/{country_en}_{target_chunk+17}.xlsx\'.')


# ------------------------------------------------------ #
