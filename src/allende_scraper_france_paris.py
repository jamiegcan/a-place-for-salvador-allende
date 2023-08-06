# allende-scraper-france-paris.py
# Main repo: https://github.com/GoGroGlo/a-place-for-salvador-allende

# Automates the data collection by verifying using https://www.openstreetmap.org
# the list of links that weren't already captured in 
# allende_scraper_france_streets.py and allende_scraper_france_links.py via 
# http://www.abacq.org/calle/index.php?2007/03/09/49-la-region-parisina-francia 


# ------------------------------------------------------ #


### IMPORTS ###


# web scraping tutorial courtesy of 
# https://www.educative.io/blog/python-web-scraping-tutorial

# standard library imports
import re

# third party imports
import unidecode
import pandas as pd 
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

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

# the source of allende_in_france_paris.txt
default_link = 'http://www.abacq.org/calle/index.php?2007/03/09/49-la-region-parisina-francia'


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


### FUNCTIONS ###


# create a Firefox driver object
def create_driver():
    s = Service()
    global driver
    driver = webdriver.Firefox(service=s)


# maximize window for every open page
def browser_window(link):
    driver.get(link)
    driver.maximize_window()


# modified OpenStreetMap checker of locale from allende_in_france_locales.txt
def osm_check(locale_1, data):

    # trim the zip code away for later use
    global locale_1_no_zip
    locale_1_no_zip = re.search(r'(.*?),*\s+', locale_1)
    locale_1_no_zip = str(locale_1_no_zip.group(1))
    
    # store search results here 
    locale_results_list = []

    # cross-check locale with OpenStreetMap
    # first, do a specific search for 
    # 'Salvador Allende [zip code] [locale] France'
    locale_link = f'https://www.openstreetmap.org/search?query=Salvador%20Allende%20{locale_1}%20{country_en}'
    browser_window(locale_link)

    # humanizer fixes the problem of the script getting no OSM info sometimes 
    # when you can see in the browser that there actually is
    asm.humanizer(timer)

    osm_soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=SoupStrainer(
        "ul", class_="results-list list-group list-group-flush"))

    # collect search results
    locale_results_list.extend(
        list(osm_soup.find_all("a", class_="set_position")))

    # if the first search has no results, try a more general search for 
    # 'Allende [zip code] [locale] France'
    if len(locale_results_list) == 0:
        locale_link = f'https://www.openstreetmap.org/search?query=Allende%20{locale_1}%20{country_en}'
        browser_window(locale_link)

        # humanizer fixes the problem of the script getting no OSM info sometimes 
        # when you can see in the browser that there actually is
        asm.humanizer(timer)

        osm_soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=SoupStrainer(
            "ul", class_="results-list list-group list-group-flush"))
        
        # collect search results
        locale_results_list.extend(
            list(osm_soup.find_all("a", class_="set_position")))
        
    # if still no results, try 
    # 'Salvador Allende [locale] France' (without the zip code)
    if len(locale_results_list) == 0:
        locale_link = f'https://www.openstreetmap.org/search?query=Salvador%20Allende%20{locale_1_no_zip}%20{country_en}'
        browser_window(locale_link)

        # humanizer fixes the problem of the script getting no OSM info sometimes 
        # when you can see in the browser that there actually is
        asm.humanizer(timer)

        osm_soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=SoupStrainer(
            "ul", class_="results-list list-group list-group-flush"))
        
        # collect search results
        locale_results_list.extend(
            list(osm_soup.find_all("a", class_="set_position")))
        
    # and then 'Allende [locale] France' (without the zip code)
    if len(locale_results_list) == 0:
        locale_link = f'https://www.openstreetmap.org/search?query=Allende%20{locale_1_no_zip}%20{country_en}'
        browser_window(locale_link)

        # humanizer fixes the problem of the script getting no OSM info sometimes when you can see in the browser that there actually is
        asm.humanizer(timer)

        osm_soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=SoupStrainer(
            "ul", class_="results-list list-group list-group-flush"))
        
        # collect search results
        locale_results_list.extend(
            list(osm_soup.find_all("a", class_="set_position")))

    # a single result looks like the one below
    # we can derive lots of info from here once user verifies that it looks good

    # <a class="set_position" data-lat="-12.1102763" data-lon="-77.0104283"
    # data-min-lat="-12.1103037" data-max-lat="-12.1102452" 
    # data-min-lon="-77.0109212" data-max-lon="-77.0097999"
    # data-prefix="Residential Road" data-name="Salvador Allende, Villa Victoria, 
    # Surquillo, Province of Lima, Lima Metropolitan Area, Lima, 15000, Peru"
    # data-type="way" data-id="426845566" href="/way/426845566">Salvador Allende, 
    # Villa Victoria, Surquillo, Province of Lima, Lima Metropolitan Area, Lima, 15000, Peru</a>
    
    # if there are no search results at all
    if len(locale_results_list) == 0:
        print('No addresses found in OpenStreetMap. Will use the locale derived from the article...')
        data['locale_1'].append(locale_1_no_zip)
        print(f'Locale 1: {locale_1_no_zip}')
        # clear the previous entry's osm_address and osm_info 
        # so that it doesn't get copied into the current entry
        global osm_address
        osm_address = ''
        global osm_info
        osm_info = ''

    # else, if there is at least one search result
    else:
        print(
            f'{str(len(locale_results_list))} possible address(es) found in OpenStreetMap.')
        for result in locale_results_list:
            result = str(result)
            osm_address = re.search(r'>\"*(.*)\"*<\/a>', result)
            osm_address = str(osm_address.group(1))
            
            # have user verify the address 
            # this decides what this loop should do next
            print(
                f'Please verify if this address matches the place in this article:\n{osm_address}')
            user_verification = input(
                '>>> Type y if yes, n if no: ')
            # typo prevention
            while user_verification != 'n' and user_verification != 'y':
                user_verification = input(
                    '>>> Try again - Type y if yes, n if no: ')
            
            # if there is only one result and it doesn't match the article's place
            if user_verification == 'n' and len(locale_results_list) == 1:
                print('OpenStreetMap address does not match the place in this article. Will use the locale derived from the article...')
                # clear the previous entry's osm_address and osm_info
                # so that it doesn't get copied into the current entry
                osm_address = ''
                osm_info = ''
                data['locale_1'].append(locale_1_no_zip)
                print(f'Locale 1: {locale_1_no_zip}')
                break
            
            # if result matches article's place
            elif user_verification == 'y':
                # we'll save the whole result in a variable for later parsing.
                # we can then close the loop.
                osm_info = result
                break
            
            # if there are more than one result and we haven't exhausted the loop yet
            elif user_verification == 'n' and len(locale_results_list) > 1:
                # clear the previous entry's osm_address and osm_info
                # so that it doesn't get copied into the current entry
                osm_address = ''
                osm_info = ''
                continue
    
        # if we have exhausted all list items and none of them matches the place
        else:
            print('All OpenStreetMap addresses do not match the place in this article. Will use the locale derived from the article...')
            # clear the previous entry's osm_address and osm_info 
            # so that it doesn't get copied into the current entry
            osm_address = ''
            osm_info = ''
            # nothing else we can do but add the default locale_1
            data['locale_1'].append(locale_1_no_zip)
            print(f'Locale 1: {locale_1_no_zip}')

        # stay in the web page like a normal human would
        asm.humanizer(timer)
        # then go on with our automated lives
        
        # when we have osm_info, we'll take locale details from its osm_address by splitting it.
        # sample split:
        # ['Salvador Allende', 'Villa Victoria', 'Surquillo', 'Province of Lima', 
        # 'Lima Metropolitan Area', 'Lima', '15000', 'Peru']
        # index 0 is the place's name, -1 is the country, -2 is the zip code, -3 is locale_1, etc...
        try:
            osm_address = osm_address.split(', ')
            locale_1 = osm_address[-3]
            data['locale_1'].append(locale_1)
            print(f'Locale 1: {locale_1}')
        except:
            pass


# modified extract_osm_info
def extract_osm_info(data):

    # get LOCALE_2
    global locale_2
    try:
        locale_2 = osm_address[-4]
    except:
        locale_2 = ''
    data['locale_2'].append(locale_2)
    print(f'Locale 2: {locale_2}')
    
    # get LOCALE_3
    global locale_3
    try:
        locale_3 = osm_address[-5]
    except:
        locale_3 = ''
    data['locale_3'].append(locale_3)
    print(f'Locale 3: {locale_3}')
    
    # get LOCALE_4
    global locale_4
    try:
        locale_4 = osm_address[-6]
    except:
        locale_4 = ''
    data['locale_4'].append(locale_4)
    print(f'Locale 4: {locale_4}')
    
    # get LOCALE_5
    global locale_5
    try:
        locale_5 = osm_address[-7]
    except:
        locale_5 = ''
    data['locale_5'].append(locale_5)
    print(f'Locale 5: {locale_5}')

    # get ZIP_CODE
    # if there is no OSM result, get the zip code from allende_in_france_locales.txt
    # if there is still none from that file, leave zip_code blank
    global zip_code
    try:
        zip_code = osm_address[-2]
    except:
        try:
            zip_code = re.search(r'(\d{5})', locale)
            zip_code = str(zip_code.group(1))
        except:
            zip_code = ''
    data['zip_code'].append(zip_code)
    print(f'Zip code: {zip_code}')

    # get LATITUDE
    global latitude
    try:
        latitude = re.search(r'data-lat="(.*?)"', osm_info)
        latitude = float(latitude.group(1))
    except:
        latitude = ''
    data['latitude'].append(latitude)
    print(f'Latitude: {latitude}')

    # get LONGITUDE
    global longitude
    try:
        longitude = re.search(r'data-lon="(.*?)"', osm_info)
        longitude = float(longitude.group(1))
    except:
        longitude = ''
    data['longitude'].append(longitude)
    print(f'Longitude: {longitude}')


# get corresponding abacq link for a locale
def get_abacq_link(locale_1_no_zip):

    # make text searchable within the URL by lowercasing and doing substitutions
    search_in_url = locale_1_no_zip.lower()
    search_in_url = unidecode.unidecode(search_in_url)
    search_in_url = search_in_url.replace('\'', '-')
    search_in_url = search_in_url.replace(' / ', '-')
    search_in_url = search_in_url.replace(' ', '-')

    # create a list of links for review
    links_for_review = []

    # clear links_for_review from the previous locale iteration
    links_for_review.clear()

    # create variable
    global abacq_reference

    # look for URL matches
    with open('france\\allende_in_france_links.txt', 'r', encoding="utf=8") as f:
        for l in f.readlines():
            l = l.strip()
            if search_in_url in l:
                links_for_review.append(l)

    # review the links
    if len(links_for_review) == 0:
        print('No abacq links found, though this could be wrong - please review later.')
        abacq_reference = default_link
        data['abacq_reference'].append(abacq_reference)
        print(f'abacq reference: {abacq_reference}')
    elif len(links_for_review) > 0:
        print(
            f'{len(links_for_review)} abacq links found - please review the following:')
        for (i, l) in enumerate(links_for_review, start=1):
            print(f'{i} : {l}')

        # let user choose which link to put in abacq_reference
        # usually this would be the link that gives the most information about the locale
        user_choice = int(
            input(
            '>>> Which link to put as abacq_reference? (type one of the numbers above or zero (0) for the default link): '))


        # if zero was pressed, assign default_link as abacq_reference
        if user_choice == 0:
            abacq_reference = default_link
            data['abacq_reference'].append(abacq_reference)
            print(f'abacq reference: {abacq_reference}')
        else:
            # else, assign a specific link to abacq_reference
            try:
                abacq_reference = links_for_review[user_choice-1]
            except:
                # typo prevention
                user_choice = int(
                    input(
                    '>>> Try again - Which link to put as abacq_reference? (type one of the numbers above or zero (0) for the default link): '))
            else:
                data['abacq_reference'].append(abacq_reference)
                print(f'abacq reference: {abacq_reference}')

    # create another list of links that were caught here
    # anything not caught here will be reviewed separately
    #
    # edit: can't seem to get this working as intended;
    # commenting this out for now.
    # let's just collect the distinct links from France_all.xlsx 
    # and compare them with allende_in_france_links.txt for future scraping
    #
    # global links_in_locales
    # links_in_locales = []
    # if len(links_for_review) > 0:
    #     links_in_locales.extend(links_for_review)


# browse abacq_reference only if it's not the default link
def browse_abacq(abacq_reference):

    if str(abacq_reference) != str(default_link):

        browser_window(abacq_reference)

        # we are only interested in the article itself, 
        # not the comments, sidebar, etc.
        global article_soup
        article_soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=SoupStrainer(
            "div", class_="post"))
        
        # stay in the web page like a normal human would
        asm.humanizer(timer)

        # then go on with our automated lives
        global text
        text = article_soup.get_text()
        global lower_text
        lower_text = text.lower()
        print(f'\n{text}')

    # fallback if abacq_reference happens to be 
    # the default link (we don't want to load this over and over again)
    else:
        article_soup = ''
        text = ''
        lower_text = ''


# modified get_name
def get_name(data):
    global name
    try:
        # get OSM name if available
        name = osm_address[0]
    except:
        # if not, get it from allende_in_france.txt
        with open('france\\allende_in_france.txt', 'r', encoding="utf=8") as f:
            for l in f.readlines():
                if locale_1_no_zip in l:
                    name = re.search(r'(.+)\s+(?:\d{5})?\s+.+(?=\.)', l)
                    name = name.group(1).strip()
    data['name'].append(name)
    print(f'Name: {name}')


# get DESC
def get_desc(article_soup, data):
        global desc
        global desc_soup
        
        # default value is blank (no desc)
        desc = ''

        # look for text in italics if any
        try:
            desc_soup = article_soup.find_all("em")
            desc_soup = list(desc_soup)
        except:
            pass
        else:
            # format them when found
            for desc_item in desc_soup:
                desc_item = str(desc_item)
                desc_item = desc_item.strip('</em>')
                desc += desc_item + '\n'
            desc = desc.replace('<br/>', '')

        # store data
        data['desc'].append(desc)
        print(f'Desc: {desc}')


# ------------------------------------------------------ #


### MAIN ###

### PREPARE LISTS ###


# open and save list of locales and zip codes in the Paris region sourced from
# http://www.abacq.org/calle/index.php?2007/03/09/49-la-region-parisina-francia
# len(allende_in_france_paris) = 92
with open('france\\allende_in_france_paris.txt', 'r', encoding="utf-8") as f:
    allende_in_france_paris = []
    for l in f.readlines():
        l = l.strip()
        allende_in_france_paris.append(l)


# compare their zip codes against those in allende_in_france_locales.txt
# if the zip code is already in allende_in_france_locales.txt,
# we've done that place so it can be removed
# len(allende_in_france_paris) = 68
with open('france\\allende_in_france_locales.txt', 'r', encoding="utf-8") as g:
    l_zip_codes = []
    for l in g.readlines():
        # extract the zip code
        l_zip_code = re.search(r'(?:\d{5})? *(.+)', l)
        l_zip_code = str(l_zip_code.group(1))
        l_zip_codes.append(l_zip_code)

for l_zip_code in l_zip_codes:
    for locale in allende_in_france_paris:
        if l_zip_code in locale:
            allende_in_france_paris.remove(locale)


# now, compare the locale name against those in allende_in_france_links.txt
# if the locale name is already in allende_in_france_links.txt
# we've done that place so it can be removed
# len(allende_in_france_paris) = 26, good enough for one sitting
with open('france\\allende_in_france_links.txt','r') as h:
    l_locale_urls = []
    for l in h.readlines():
        l = l.strip()
        l_locale_urls.append(l)

# skip links_exceptions
for i in links_exceptions[:]:
    for l in l_locale_urls[:]:
        if i in l:
            l_locale_urls.remove(l)


# compare sanitized locales against every url
for l in l_locale_urls[:]:
    # extract and sanitize locale names from allende_in_france_paris
    for locale in allende_in_france_paris[:]:
        # extract part
        _i = re.search(r'\d+\.\s+(.*?),*\s+', locale)
        _i = str(_i.group(1))
        # sanitize part
        _i = _i.lower()
        _i = unidecode.unidecode(_i)
        _i = _i.replace('\'', '-')
        _i = _i.replace(' / ', '-')
        _i = _i.replace(' ', '-')
        # remove if a match is found
        if _i in l:
            allende_in_france_paris.remove(locale)


# ------------------------------------------------------ #


### WORK WITH EACH LOCALE ###


# start the browser
try:
    create_driver()


    for (i, locale) in enumerate(allende_in_france_paris, start=1):


        # skip if whitespace
        if locale == '' or locale == '\n':
            continue


        # skip if locale doesn't contain allende
        if 'Allende' not in locale:
            continue


        # sanitize and print current locale
        locale = locale.strip()
        locale = re.search(r'\d+\. (.* \d+)', locale)
        locale = str(locale.group(1))
        print('\n')
        print('--------------------------------------------------------------------------------------------')
        print(f'Processing locale {i} of {len(allende_in_france_paris)} : {locale}')
        print('--------------------------------------------------------------------------------------------')
        print('\n')


        # get ID (null)
        id = ''
        data['id'].append(id)
        print(f'ID: {id}')


        # get COUNTRY and REGION
        data['country'].append(country_en)
        print(f'Country: {country_en}')

        data['region'].append(region)
        print(f'Region: {region}')


        # load OSM and search for the locale
        osm_check(locale, data)


        # extract OSM info if any
        extract_osm_info(data)


        # get and review abacq links if any
        # abacq_reference also gets assigned here
        get_abacq_link(locale_1_no_zip)


        # browse the chosen abacq link
        browse_abacq(abacq_reference)


        # get NAME
        get_name(data)

        
        # get TYPE
        asm.get_type(osm_info, name, data)


        # get DESC
        get_desc(article_soup, data)


        # get DESC_LANGUAGE (null)
        # won't assume anything here for now because 
        # most of the descriptions I see are in Spanish, regardless of the region
        desc_language = ''
        data['desc_language'].append(desc_language)
        print(f'Desc language: {desc_language}')

        
        # get OLDEST_KNOWN_YEAR
        asm.get_oldest_known_year(abacq_reference, text, data)

        
        # get OLDEST_KNOWN_MONTH
        asm.get_oldest_known_month(abacq_reference, lower_text, data)

        
        # get OLDEST_KNOWN_DAY
        asm.get_oldest_known_day(abacq_reference, lower_text, data)

        
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
        asm.get_verified_in_maps_and_osm_link(osm_info, data)

        
        # get GOOGLE_MAPS_LINK (null)
        google_maps_link = ''
        data['google_maps_link'].append(google_maps_link)
        print(f'Google Maps link: {google_maps_link}')

        
        # stay in the web page like a normal human would
        asm.humanizer(timer)


# quit the browser properly regardless of whether it returns an exception
finally:
    driver.quit()


# ------------------------------------------------------ #


### EXPORT THE DATA ###


# create a dataframe of all info collected
data_df = pd.DataFrame(data=data)
print('\nDataFrame created:\n')
print(data_df)


# export dataframe - xlsx supports unicode, 
# so no more encoding fiascos compared to saving to csv.
# suffixed with 21 because allende_scraper_france_streets.py
# and allende_scraper_france_links.py together made 20 chunks

# data_df.to_excel(
#     f'test_files/{country_en}_{target_chunk}.xlsx', index=False) # for test files
data_df.to_excel(
    f'countries/{country_en}_21.xlsx', index=False) # for main files
print(
    f'DataFrame saved in \'countries/{country_en}_21.xlsx\'.')


# ------------------------------------------------------ #
