# allende-scraper-main.py
# 'production' script

# web scraping tutorial courtesy of https://www.educative.io/blog/python-web-scraping-tutorial


from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import re
import pandas as pd


# countries with a Salvador Allende presence, according to http://www.abacq.org/calle/index.php?toc/toc
allende_countries = {
    'Alemania': {
        'country_en': 'Germany',
        'country_link': 'alemania',
        'region': 'Europe'
    },
    'Angola': {
        'country_en': 'Angola',
        'country_link': 'angola',
        'region': 'Africa'
    },
    'Arabia Saudita': {
        'country_en': 'Saudi Arabia',
        'country_link': 'arabia-saudita',
        'region': 'Middle East'
    },
    'Argelia': {
        'country_en': 'Algeria',
        'country_link': 'argelia',
        'region': 'Africa'
    },
    'Argentina': {
        'country_en': 'Argentina',
        'country_link': 'argentina',
        'region': 'South America'
    },
    'Australia': {
        'country_en': 'Australia',
        'country_link': 'australia',
        'region': 'ANZ and Oceania'
    },
    'Austria': {
        'country_en': 'Austria',
        'country_link': 'austria',
        'region': 'Europe'
    },
    'Bélgica': {
        'country_en': 'Belgium',
        'country_link': 'belgica',
        'region': 'Europe'
    },
    'Bosnia-Herzegovina': {
        'country_en': 'Bosnia and Herzegovina',
        'country_link': 'bosnia-herzegovina',
        'region': 'Europe'
    },
    'Brasil': {
        'country_en': 'Brazil',
        'country_link': 'brasil',
        'region': 'South America'
    },
    'Bulgaria': {
        'country_en': 'Bulgaria',
        'country_link': 'bulgaria',
        'region': 'Europe'
    },
    'Canadá': {
        'country_en': 'Canada',
        'country_link': 'canada',
        'region': 'North America'
    },
    'Chile': {
        'country_en': 'Chile',
        'country_link': 'chile',
        'region': 'South America'
    },
    'Colombia': {
        'country_en': 'Colombia',
        'country_link': 'colombia',
        'region': 'South America'
    },
    'Cuba': {
        'country_en': 'Cuba',
        'country_link': 'cuba',
        'region': 'Central America'
    },
    'Dinamarca': {
        'country_en': 'Denmark',
        'country_link': 'dinamarca',
        'region': 'Europe'
    },
    'Ecuador': {
        'country_en': 'Ecuador',
        'country_link': 'ecuador',
        'region': 'South America'
    },
    'Eslovaquia': {
        'country_en': 'Slovakia',
        'country_link': 'eslovaquia',
        'region': 'Europe'
    },
    'España': {
        'country_en': 'Spain',
        'country_link': 'espana',
        'region': 'Europe'
    },
    'Estados Unidos': {
        'country_en': 'United States',
        'country_link': 'estados-unidos',
        'region': 'North America'
    },
    'Francia': {
        'country_en': 'France',
        'country_link': 'francia',
        'region': 'Europe'
    },
    'Guinea-Bissáu': {
        'country_en': 'Guinea-Bissau',
        'country_link': 'guinea-bissau',
        'region': 'Africa'
    },
    'Holanda': {
        'country_en': 'Netherlands',
        'country_link': 'holanda',
        'region': 'Europe'
    },
    'Hungría': {
        'country_en': 'Hungary',
        'country_link': 'hungria',
        'region': 'Europe'
    },
    'India': {
        'country_en': 'India',
        'country_link': 'india',
        'region': 'Asia'
    },
    'Irán': {
        'country_en': 'Iran',
        'country_link': 'iran',
        'region': 'Asia'
    },
    'Israel': {
        'country_en': 'Israel',
        'country_link': 'israel',
        'region': 'Middle East'
    },
    'Italia': {
        'country_en': 'Italy',
        'country_link': 'italia',
        'region': 'Europe'
    },
    'Luxemburgo': {
        'country_en': 'Luxembourg',
        'country_link': 'luxemburgo',
        'region': 'Europe'
    },
    'México': {
        'country_en': 'Mexico',
        'country_link': 'mexico',
        'region': 'North America'
    },
    'Mozambique': {
        'country_en': 'Mozambique',
        'country_link': 'mozambique',
        'region': 'Africa'
    },
    'Nicaragua': {
        'country_en': 'Nicaragua',
        'country_link': 'nicaragua',
        'region': 'Central America'
    },
    'Pakistán': {
        'country_en': 'Pakistan',
        'country_link': 'pakistan',
        'region': 'Asia'
    },
    'Palestina': {
        'country_en': 'Palestine',
        'country_link': 'palestina',
        'region': 'Middle East'
    },
    'Paraguay': {
        'country_en': 'Paraguay',
        'country_link': 'paraguay',
        'region': 'South America'
    },
    'Perú': {
        'country_en': 'Peru',
        'country_link': 'peru',
        'region': 'South America'
    },
    'Portugal': {
        'country_en': 'Portugal',
        'country_link': 'portugal',
        'region': 'Europe'
    },
    'Reino Unido': {
        'country_en': 'United Kingdom',
        'country_link': 'reino-unido',
        'region': 'Europe'
    },
    'República Checa': {
        'country_en': 'Czechia',
        'country_link': 'republica-checa',
        'region': 'Europe'
    },
    'República del Congo': {
        'country_en': 'Republic of the Congo',
        'country_link': 'republica-del-congo',
        'region': 'Africa'
    },
    'República de Macedonia': {
        'country_en': 'North Macedonia',
        'country_link': 'macedonia',
        'region': 'Europe'
    },
    'República Dominicana': {
        'country_en': 'Dominican Republic',
        'country_link': 'republica-dominicana',
        'region': 'Asia'
    },
    'Rusia': {
        'country_en': 'Russia',
        'country_link': 'rusia',
        'region': 'Europe'
    },
    'Salvador': {
        'country_en': 'El Salvador',
        'country_link': 'el-salvador',
        'region': 'Central America'
    },
    'Serbia': {
        'country_en': 'Serbia',
        'country_link': 'serbia',
        'region': 'Europe'
    },
    'Turquía': {
        'country_en': 'Turkey',
        'country_link': 'turquia',
        'region': 'Middle East'
    },
    'Uruguay': {
        'country_en': 'Uruguay',
        'country_link': 'uruguay',
        'region': 'South America'
    },
    'Venezuela': {
        'country_en': 'Venezuela',
        'country_link': 'venezuela',
        'region': 'South America'
    }
}


# non-exhaustive lists of words that correspond to a specific type of establishment
types = {
    'street'                : ['calle', 'avenida', 'pasaje', 'rue', 'rua', 'road', 'avenue', 'circunvalación', 'boulevard', 'bulevar', 'street', 'straat', 'strada'],
    'monument'              : ['monumento', 'escultura', 'monument', 'sculpture', 'busto', 'bust', 'statue'],
    'park'                  : ['plaza', 'parque', 'square', 'park', 'place', 'plazoleta'],
    'school'                : ['escuela', 'colegio', 'school', 'college', 'schule', 'école'],
    'healthcare facility'   : ['hospital', 'salud', 'healthcare', 'health'],
    'bridge'                : ['puente', 'bridge', 'pont', 'brücke'],
    'sports center'         : ['complexe sportif', 'sports complex', 'sport', 'sports', 'sports center', 'sports centre',  'complejo de deporte'],
    'multipurpose center'   : ['espace', 'hall'],
    'port'                  : ['puerto', 'port'],
    'neighborhood'          : ['población', 'village', 'hamlet'],
    'museum'                : ['museo', 'museum' , 'musée']
}


months = {
    'enero'         : int(1),
    'febrero'       : int(2),
    'marzo'         : int(3),
    'abril'         : int(4),
    'mayo'          : int(5),
    'junio'         : int(6),
    'julio'         : int(7),
    'agosto'        : int(8),
    'septiembre'    : int(9),
    'octubre'       : int(10),
    'noviembre'     : int(11),
    'diciembre'     : int(12),
    '01'            : int(1),
    '02'            : int(2),
    '03'            : int(3),
    '04'            : int(4),
    '05'            : int(5),
    '06'            : int(6),
    '07'            : int(7),
    '08'            : int(8),
    '09'            : int(9),
    '10'            : int(10),
    '11'            : int(11),
    '12'            : int(12)
}


days = {
    '01'    : int(1),
    '02'    : int(2),
    '03'    : int(3),
    '04'    : int(4),
    '05'    : int(5),
    '06'    : int(6),
    '07'    : int(7),
    '08'    : int(8),
    '09'    : int(9)
}



# ------------------------------------------------------ #



### 1. RETRIEVE ALL LINKS ###


# create a Google Chrome driver object
# https://stackoverflow.com/questions/69918148/deprecationwarning-executable-path-has-been-deprecated-please-pass-in-a-servic
s = Service('C:\\Users\\canogle\\.cache\\selenium\\chromedriver\\win32\\110.0.5481.77\\chromedriver.exe')
driver = webdriver.Chrome(service=s)


# base URLs
homepage = 'http://www.abacq.org'
toc = 'http://www.abacq.org/calle/index.php?toc/toc'


# fetch all urls from the site map
driver.get(toc)
soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=SoupStrainer("div", id="toc"))


# all links are under an <li> tag
links_soup = soup.find_all("li")
print(f'>>> Parsing the site map {toc}...\n')
# print(links_soup, '\n')


# create a list of bare links
links_list = []

for link in links_soup:
    link = str(link)
    link = re.search(r'(\/calle\/index.php\?\d{4}\/\d{2}\/\d{2}\/\d*(?:-\w*)*)', link)
    link = str(homepage) + str(link.group(1))
    links_list.append(link)
print('>>> Fetching all links...')
print(f'{str(len(links_list))} links found.\n')
# print(links_list, '\n')



# ------------------------------------------------------ #



### 2. GROUP LINKS BY COUNTRY ###


countries_links = {
    'Alemania'                  : [],
    'Angola'                    : [],
    'Arabia Saudita'            : [],
    'Argelia'                   : [],
    'Argentina'                 : [],
    'Australia'                 : [],
    'Austria'                   : [],
    'Bélgica'                   : [],
    'Bosnia-Herzegovina'        : [],
    'Brasil'                    : [],
    'Bulgaria'                  : [],
    'Canadá'                    : [],
    'Chile'                     : [],
    'Colombia'                  : [],
    'Cuba'                      : [],
    'Dinamarca'                 : [],
    'Ecuador'                   : [],
    'Eslovaquia'                : [],
    'España'                    : [],
    'Estados Unidos'            : [],
    'Francia'                   : [],
    'Guinea-Bissáu'             : [],
    'Holanda'                   : [],
    'Hungría'                   : [],
    'India'                     : [],
    'Irán'                      : [],
    'Israel'                    : [],
    'Italia'                    : [],
    'Luxemburgo'                : [],
    'México'                    : [],
    'Mozambique'                : [],
    'Nicaragua'                 : [],
    'Pakistán'                  : [],
    'Palestina'                 : [],
    'Paraguay'                  : [],
    'Perú'                      : [],
    'Portugal'                  : [],
    'Reino Unido'               : [],
    'República Checa'           : [],
    'República del Congo'       : [],
    'República de Macedonia'    : [],
    'República Dominicana'      : [],
    'Rusia'                     : [],
    'Salvador'                  : [],
    'Serbia'                    : [],
    'Turquía'                   : [],
    'Uruguay'                   : [],
    'Venezuela'                 : []
}


# assign links according to the country in their url
for link in links_list:
    for key in allende_countries.keys():
        if allende_countries[key]['country_link'] in link:
            countries_links[key].append(link)


# enter here the country name (in Spanish) you want to do
print('Available countries for processing:\n')
for key in allende_countries.keys():
    print(key)
country = str(input('>>> Please enter one of the countries above: '))

if country not in allende_countries.keys():
    raise Exception(f'{country} is not available.')


# retrieve the links for that country
print(f'>>> Fetching links for this country...')
# print(countries_links[country])


# most links have the format http://www.abacq.org/calle/index.php?2009/11/06/435-sierra-gorda-chile
# this corresponds to one locale in one country.
# links with this format http://www.abacq.org/calle/index.php?2009/01/08/303-chile
# contains multiple locales within one country.
#
# sort links according to whether they're single-locale or multi-locale

single_locale = []
multi_locale = []

for link in countries_links[country]:
    link_check = re.search(r'(\/calle\/index.php\?\d{4}\/\d{2}\/\d{2}\/\d*(?:-\w*){2,})', link)
    if link_check is None:
        multi_locale.append(link)
    else:
        single_locale.append(link)

print(f'{str(len(countries_links[country]))} links found: {str(len(single_locale))} single-locale, {str(len(multi_locale))} multi-locale.\n')
print(f'Single-locale links:\n{single_locale}\n')
print(f'Multi-locale links:\n{multi_locale}\n')



# ------------------------------------------------------ #



### 3. SCRAPE EVERY LINK IN A BATCH ###


### WHAT TO COLLECT ###

# for each post, let's collect the following and connect them with the existing columns from the current db:
# name - image_alt - <img alt=[alt]>
# type - derived from the post's name and/or text
# _region - derived from allende_countries
# country - country - regex-ed from post title <h2 class="post-title">
# locale - <strong>
# oldest_known_year,month,day - scraped from the post's text
# desc - desc - <em>
# abacq-reference - post_url - <h2><a href=[]>


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



### SINGLE-LOCALE SCRAPER ###


# every link is basically an article so we'll retrieve their contents
for (i, link) in enumerate(single_locale, start=1):
    driver.get(link)

    #
    # we are only interested in the article itself, not the comments, sidebar, etc.
    #
    article_soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=SoupStrainer("div", class_="post")) #, from_encoding='windows-1252', exclude_encodings=['unicode', 'utf-8'])
    print(f'\n>>> Parsing single-locale article {str(i)} of {str(len(single_locale))}: {link}...\n')
    text = article_soup.get_text()
    lower_text = text.lower()
    print(text)

    #
    # get ID (null)
    #
    id = ''
    data['id'].append(id)
    print(f'ID: {id}')

    #
    # get COUNTRY
    #
    country_es = article_soup.find("h2", class_="post-title")
    country_es = str(country_es)
    country_es = re.search(r'(?:\.|,)\s*(.*)<\/h2>', country_es)
    country_es = str(country_es.group(1))
    country_en = allende_countries[country_es]['country_en']
    data['country'].append(country_en)
    print(f'Country: {country_en}')

    #
    # get REGION
    #
    region = allende_countries[country_es]['region']
    data['region'].append(region)
    print(f'Region: {region}')

    #
    # get LOCALE_1
    # we'll take the locale found in abacq as the default locale_1
    #
    locale_1 = article_soup.find("strong")
    locale_1 = str(locale_1)
    locale_1 = re.search(r'<strong>(.*)<\/strong>', locale_1)
    try:
        str(locale_1.group(1))
    except:
        locale_1 = article_soup.find("h2", class_="post-title")
        locale_1 = str(locale_1)
        locale_1 = re.search(r'<h2 class="post-title">(.*)(?:\.|,)\s*.*<\/h2>', locale_1)
        locale_1 = str(locale_1.group(1))
    else:
        locale_1 = str(locale_1.group(1))
    #
    # when we have this abacq locale, we then cross-check this with OpenStreetMap
    #
    locale_link = f'https://www.openstreetmap.org/search?query=Salvador%20Allende%20{locale_1}%20{country_en}'
    driver.get(locale_link)
    osm_soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=SoupStrainer("div", class_="search_results_entry mx-n3"))
    osm_text = osm_soup.get_text()
    #
    # if there are no results found, keep the default locale=1
    #
    if 'No results found' in osm_text:
        print('No addresses found in OpenStreetMap. Will use the locale derived from the article...')
        data['locale_1'].append(locale_1)
        print(f'Locale 1: {locale_1}')
    #
    # else, go through each search result and have the user verify it
    #
    else:
        locale_results_list = osm_soup.find_all("a")
        # a single result looks like this - we can derive lots of info from here once user verifies that it looks good
        #
        # <a class="set_position" data-lat="-12.1102763" data-lon="-77.0104283" 
        # data-min-lat="-12.1103037" data-max-lat="-12.1102452" data-min-lon="-77.0109212" data-max-lon="-77.0097999" 
        # data-prefix="Residential Road" data-name="Salvador Allende, Villa Victoria, Surquillo, Province of Lima, Lima Metropolitan Area, Lima, 15000, Peru" 
        # data-type="way" data-id="426845566" href="/way/426845566">Salvador Allende, Villa Victoria, Surquillo, Province of Lima, Lima Metropolitan Area, Lima, 15000, Peru</a>
        #
        if len(locale_results_list) == 0:
            print('No addresses found in OpenStreetMap. Will use the locale derived from the article...')
            data['locale_1'].append(locale_1)
            print(f'Locale 1: {locale_1}')
        else:
            print(f'{str(len(locale_results_list)-1)} possible address(es) found in OpenStreetMap.')
            for result in locale_results_list:
                result = str(result)
                osm_address = re.search(r'data-name="(.*?)"', result)
                osm_address = str(osm_address.group(1))
                #
                # have user verify the address - this decides what this loop should do next
                #
                print(f'Please verify if this address matches the place in this article:\n{osm_address}')
                user_verification = input('>>> Type y if yes, n if no: ')
                if user_verification == 'n' and len(locale_results_list) == 1:
                    print('OpenStreetMap address does not match the place in this article. Will use the locale derived from the article...')
                    data['locale_1'].append(locale_1)
                    print(f'Locale 1: {locale_1}')
                elif user_verification == 'n' and len(locale_results_list) > 1:
                    continue
                elif user_verification == 'y':
                    # we'll save the whole result in a variable for later parsing. we can then close the loop.
                    osm_info = result
                    break

        #
        # when we have osm_info, we'll take locale details from its osm_address by splitting it.
        # sample split:
        # ['Salvador Allende', 'Villa Victoria', 'Surquillo', 'Province of Lima', 'Lima Metropolitan Area', 'Lima', '15000', 'Peru']
        # index 0 is the place's name, -1 is the country, -2 is the zip code, -3 is locale_1, etc...
        #
        try:
            osm_address = osm_address.split(', ')
            locale_1 = osm_address[-3]
            data['locale_1'].append(locale_1)
            print(f'Locale 1: {locale_1}')
        except:
            pass

    #
    # if the place has an OSM link, we'll get values from there. otherwise, we'll take from the article or make the value null.
    #

    #
    # get LOCALE_2
    #
    try:
        locale_2 = osm_address[-4]
    except:
        locale_2 = ''
    data['locale_2'].append(locale_2)
    print(f'Locale 2: {locale_2}')

    #
    # get LOCALE_3
    #
    try:
        locale_3 = osm_address[-5]
    except:
        locale_3 = ''
    data['locale_3'].append(locale_3)
    print(f'Locale 3: {locale_3}')

    #
    # get LOCALE_4
    #
    try:
        locale_4 = osm_address[-6]
    except:
        locale_4 = ''
    data['locale_4'].append(locale_4)
    print(f'Locale 4: {locale_4}')

    #
    # get LOCALE_5
    #
    try:
        locale_5 = osm_address[-7]
    except:
        locale_5 = ''
    data['locale_5'].append(locale_5)
    print(f'Locale 5: {locale_5}')

    #
    # get ZIP_CODE
    #
    try:
        zip_code = osm_address[-2]
    except:
        zip_code = ''
    data['zip_code'].append(zip_code)
    print(f'Zip code: {zip_code}')

    #
    # get LATITUDE (null)
    #
    try:
        latitude = re.search(r'data-lat="(.*?)"', osm_info)
        latitude = float(latitude.group(1))
    except:
        latitude = ''
    data['latitude'].append(latitude)
    print(f'Latitude: {latitude}')

    #
    # get LONGITUDE (null)
    #
    try:
        longitude = re.search(r'data-lon="(.*?)"', osm_info)
        longitude = float(longitude.group(1))
    except:
        longitude = ''
    data['longitude'].append(longitude)
    print(f'Longitude: {longitude}')

    #
    # get NAME
    #
    try:
        # get OSM name if available
        name = osm_address[0]
    except:
        # if not, get it from the alt text of the article's main image
        name = article_soup.find("img", alt=True)
        name = str(name)
        name = re.search(r'alt="(.*?)"\s*', name)
        try:
            name = str(name.group(1))
        except:
            # fallback for when there's neither OSM name nor alt text
            name = 'A memorial to Salvador Allende'
    data['name'].append(name)
    print(f'Name: {name}')

    #
    # get TYPE
    # the dict used here is pretty rudimentary so this is prone to errors and needs human verification
    #
    type = ''
    # get OSM type if available
    try:
        type = re.search(r'data-prefix="(.*?)"', osm_info)
        type = str(type.group(1))
    except:
        # if not, derive it from NAME (which itself is either from OSM or the article)
        for key, value in types.items():
            for type_item in value:
                if type_item in name.lower():
                    type = key
    else:
        for key, value in types.items():
            for type_item in value:
                if type_item in type.lower():
                    type = key
    data['type'].append(type)
    print(f'Type: {type}')

    #
    # get OLDEST_KNOWN_YEAR
    # retrieve the year from the url; when an older year is found within the text, get that instead
    #
    oldest_known_year = re.search(r'(\d{4})', link)
    oldest_known_year = int(oldest_known_year.group(1))
    years_in_text = re.findall(r'\d{4}', text)
    years_in_text = list(years_in_text)
    for year in years_in_text:
        year = int(year)
        if year < oldest_known_year and year > int(1973):
            oldest_known_year = year
    data['oldest_known_year'].append(oldest_known_year)
    print(f'Oldest known year: {oldest_known_year}')

    #
    # get OLDEST_KNOWN_MONTH
    # retrieve the month from the url; when another month is found within the text, get that instead
    # unlike in oldest_known_year (more straightforward), we will list all months in the text if they're not the same as the one in the url
    #
    oldest_known_month = re.search(r'\d{4}\/(\d{2})\/\d{2}', link)
    oldest_known_month = months[oldest_known_month.group(1)]
    #
    # compare oldest_known_year to the year in the url.
    # if they're different (i.e. we derived the year from the text), we'll proceed with collecting months_in_text.
    #
    year_in_url = re.search(r'(\d{4})', link)
    year_in_url = int(year_in_url.group(1))
    months_in_text = re.findall(
        r'(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)', lower_text)
    months_in_text = list(months_in_text)
    if oldest_known_year != year_in_url and len(months_in_text) == 0:
        oldest_known_month = ''
    elif oldest_known_year != year_in_url and len(months_in_text) > 0:
        for month in months_in_text:
            list_months = []
            month = months[month]
            list_months.append(month)
        oldest_known_month = list_months
    data['oldest_known_month'].append(oldest_known_month)
    print(f'Oldest known month: {oldest_known_month}')

    #
    # get OLDEST_KNOWN_DAY
    # retrieve the day from the url; when another day is found within the text, get that instead
    # unlike in oldest_known_year (more straightforward), we will list all days in the text if they're not the same as the one in the url
    #
    oldest_known_day = re.search(r'\d{4}\/\d{2}\/(\d{2})', link)
    oldest_known_day = str(oldest_known_day.group(1))
    if oldest_known_day in list(days.keys()):
        oldest_known_day = days[oldest_known_day]
    else:
        oldest_known_day = int(oldest_known_day)
    #
    # compare oldest_known_year to the year in the url.
    # if they're different (i.e. we derived the year from the text), we'll proceed with collecting days_in_text.
    #
    days_in_text = re.findall(r'(\d{1,2})\s+', lower_text)
    days_in_text = list(days_in_text)
    #
    # remove numbers that are invalid days of a month
    #
    for day in days_in_text:
        if int(day) > int(31):
            days_in_text.remove(day)
    if oldest_known_year != year_in_url and len(days_in_text) == 0:
        oldest_known_day = ''
    elif oldest_known_year != year_in_url and len(days_in_text) > 0:
        for day in days_in_text:
            list_days = []
            if day in list(days.keys()):
                day = days[day]
            else:
                day = int(day)
            list_days.append(day)
        oldest_known_day = list_days
    data['oldest_known_day'].append(oldest_known_day)
    print(f'Oldest known day: {oldest_known_day}')

    #
    # get OLDEST_KNOWN_SOURCE (null)
    #
    oldest_known_source = ''
    data['oldest_known_source'].append(oldest_known_source)
    print(f'Oldest known source: {oldest_known_source}')

    #
    # get DESC
    #
    desc = ''
    desc_soup = article_soup.find_all("em")
    desc_soup = list(desc_soup)
    for desc_item in desc_soup:
        desc_item = str(desc_item)
        desc_item = desc_item.strip('</em>')
        desc += desc_item + '\n'
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
    # get VERIFIED_IN_MAPS (default to 0, will get 1 when it has OSM info)
    #
    if 'osm_info' in globals():
        verified_in_maps = 1
    else:
        verified_in_maps = 0
    data['verified_in_maps'].append(verified_in_maps)
    print(f'Verified in maps: {verified_in_maps}')

    #
    # get OPENSTREETMAP_LINK
    #
    try:
        openstreetmap_link = re.search(r'href="(.*?)"', osm_info)
        openstreetmap_link = f'https://www.openstreetmap.org{str(openstreetmap_link.group(1))}'
    except:
        openstreetmap_link = ''
    data['openstreetmap_link'].append(openstreetmap_link)
    print(f'OpenStreetMap link: {openstreetmap_link}')

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



# ------------------------------------------------------ #



### MULTI-LOCALE SCRAPER ###


# every link is basically an article so we'll retrieve their contents
for (i, link) in enumerate(multi_locale, start=1):
    driver.get(link)

    #
    # we are only interested in the article itself, not the comments, sidebar, etc.
    #
    article_soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=SoupStrainer("div", class_="post")) #, from_encoding='windows-1252', exclude_encodings=['unicode', 'utf-8'])
    print(f'\n>>> Parsing multi-locale article {str(i)} of {str(len(multi_locale))}: {link}...\n')
    text = article_soup.get_text()
    lower_text = text.lower()
    print(text)

    #
    # honestly, the multi-locale articles are less organized but are concise enough for manual human investigation.
    # each locale is still within <strong> tags so we'll take advantage of those
    #

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
    for locale_1 in locale_1_list:

        #
        # get ID (null)
        #
        id = ''
        data['id'].append(id)
        print(f'ID: {id}')

        #
        # get COUNTRY
        #
        country_es = article_soup.find("h2", class_="post-title")
        country_es = str(country_es)
        country_es = re.search(r'<h2 class="post-title">(.*?)(?:\s*\.*)*<\/h2>', country_es)
        country_es = str(country_es.group(1))
        country_en = allende_countries[country_es]['country_en']
        data['country'].append(country_en)
        print(f'Country: {country_en}')

        #
        # get REGION
        #
        region = allende_countries[country_es]['region']
        data['region'].append(region)
        print(f'Region: {region}')

        #
        # cross-check LOCALE_1 with OSM
        #
        locale_link = f'https://www.openstreetmap.org/search?query=Salvador%20Allende%20{locale_1}%20{country_en}'
        driver.get(locale_link)
        osm_soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=SoupStrainer(
            "div", class_="search_results_entry mx-n3"))
        osm_text = osm_soup.get_text()
        #
        # if there are no results found, keep the default locale_1
        #
        if 'No results found' in osm_text:
            print('No addresses found in OpenStreetMap. Will use the locale derived from the article...')
            data['locale_1'].append(locale_1)
            print(f'Locale 1: {locale_1}')
        #
        # else, go through each search result and have the user verify it
        #
        else:
            locale_results_list = osm_soup.find_all("a")
            # a single result looks like this - we can derive lots of info from here once user verifies that it looks good
            #
            # <a class="set_position" data-lat="-12.1102763" data-lon="-77.0104283"
            # data-min-lat="-12.1103037" data-max-lat="-12.1102452" data-min-lon="-77.0109212" data-max-lon="-77.0097999"
            # data-prefix="Residential Road" data-name="Salvador Allende, Villa Victoria, Surquillo, Province of Lima, Lima Metropolitan Area, Lima, 15000, Peru"
            # data-type="way" data-id="426845566" href="/way/426845566">Salvador Allende, Villa Victoria, Surquillo, Province of Lima, Lima Metropolitan Area, Lima, 15000, Peru</a>
            #
            if len(locale_results_list) == 0:
                print(
                    'No addresses found in OpenStreetMap. Will use the locale derived from the article...')
                data['locale_1'].append(locale_1)
                print(f'Locale 1: {locale_1}')
            else:
                print(
                    f'{str(len(locale_results_list)-1)} possible address(es) found in OpenStreetMap.')
                for result in locale_results_list:
                    result = str(result)
                    osm_address = re.search(r'data-name="(.*?)"', result)
                    osm_address = str(osm_address.group(1))
                    #
                    # have user verify the address - this decides what this loop should do next
                    #
                    print(
                        f'Please verify if this address matches the place in this article:\n{osm_address}')
                    user_verification = input('>>> Type y if yes, n if no: ')
                    if user_verification == 'n' and len(locale_results_list) == 1:
                        print(
                            'OpenStreetMap address does not match the place in this article. Will use the locale derived from the article...')
                        data['locale_1'].append(locale_1)
                        print(f'Locale 1: {locale_1}')
                    elif user_verification == 'n' and len(locale_results_list) > 1:
                        continue
                    elif user_verification == 'y':
                        # we'll save the whole result in a variable for later parsing. we can then close the loop.
                        osm_info = result
                        break

            #
            # when we have osm_info, we'll take locale details from its osm_address by splitting it.
            # sample split:
            # ['Salvador Allende', 'Villa Victoria', 'Surquillo', 'Province of Lima', 'Lima Metropolitan Area', 'Lima', '15000', 'Peru']
            # index 0 is the place's name, -1 is the country, -2 is the zip code, -3 is locale_1, etc...
            #
            try:
                osm_address = osm_address.split(', ')
                locale_1 = osm_address[-3]
                data['locale_1'].append(locale_1)
                print(f'Locale 1: {locale_1}')
            except:
                pass

        #
        # if the place has an OSM link, we'll get values from there. otherwise, we'll take from the article or make the value null.
        #

        #
        # get LOCALE_2
        #
        try:
            locale_2 = osm_address[-4]
        except:
            locale_2 = ''
        data['locale_2'].append(locale_2)
        print(f'Locale 2: {locale_2}')

        #
        # get LOCALE_3
        #
        try:
            locale_3 = osm_address[-5]
        except:
            locale_3 = ''
        data['locale_3'].append(locale_3)
        print(f'Locale 3: {locale_3}')

        #
        # get LOCALE_4
        #
        try:
            locale_4 = osm_address[-6]
        except:
            locale_4 = ''
        data['locale_4'].append(locale_4)
        print(f'Locale 4: {locale_4}')

        #
        # get LOCALE_5
        #
        try:
            locale_5 = osm_address[-7]
        except:
            locale_5 = ''
        data['locale_5'].append(locale_5)
        print(f'Locale 5: {locale_5}')

        #
        # get ZIP_CODE
        #
        try:
            zip_code = osm_address[-2]
        except:
            zip_code = ''
        data['zip_code'].append(zip_code)
        print(f'Zip code: {zip_code}')

        #
        # get LATITUDE (null)
        #
        try:
            latitude = re.search(r'data-lat="(.*?)"', osm_info)
            latitude = float(latitude.group(1))
        except:
            latitude = ''
        data['latitude'].append(latitude)
        print(f'Latitude: {latitude}')

        #
        # get LONGITUDE (null)
        #
        try:
            longitude = re.search(r'data-lon="(.*?)"', osm_info)
            longitude = float(longitude.group(1))
        except:
            longitude = ''
        data['longitude'].append(longitude)
        print(f'Longitude: {longitude}')

        #
        # get NAME
        #
        try:
            # get OSM name if available
            name = osm_address[0]
        except:
            # if not, get it from the alt text of the article's main image
            name = article_soup.find("img", alt=True)
            name = str(name)
            name = re.search(r'alt="(.*?)"\s*', name)
            try:
                name = str(name.group(1))
            except:
                # fallback for when there's neither OSM name nor alt text
                name = 'A memorial to Salvador Allende'
        data['name'].append(name)
        print(f'Name: {name}')

        #
        # get TYPE
        # the dict used here is pretty rudimentary so this is prone to errors and needs human verification
        #
        type = ''
        # get OSM type if available
        try:
            type = re.search(r'data-prefix="(.*?)"', osm_info)
            type = str(type.group(1))
        except:
            # if not, derive it from NAME (which itself is either from OSM or the article)
            for key, value in types.items():
                for type_item in value:
                    if type_item in name.lower():
                        type = key
        else:
            for key, value in types.items():
                for type_item in value:
                    if type_item in type.lower():
                        type = key
        data['type'].append(type)
        print(f'Type: {type}')

        #
        # get OLDEST_KNOWN_YEAR
        # retrieve the year from the url; when an older year is found within the text, get that instead
        #
        oldest_known_year = re.search(r'(\d{4})', link)
        oldest_known_year = int(oldest_known_year.group(1))
        years_in_text = re.findall(r'\d{4}', text)
        years_in_text = list(years_in_text)
        for year in years_in_text:
            year = int(year)
            if year < oldest_known_year and year > int(1973):
                oldest_known_year = year
        data['oldest_known_year'].append(oldest_known_year)
        print(f'Oldest known year: {oldest_known_year}')

        #
        # get OLDEST_KNOWN_MONTH
        # retrieve the month from the url; when another month is found within the text, get that instead
        # unlike in oldest_known_year (more straightforward), we will list all months in the text if they're not the same as the one in the url
        #
        oldest_known_month = re.search(r'\d{4}\/(\d{2})\/\d{2}', link)
        oldest_known_month = months[oldest_known_month.group(1)]
        #
        # compare oldest_known_year to the year in the url.
        # if they're different (i.e. we derived the year from the text), we'll proceed with collecting months_in_text.
        #
        year_in_url = re.search(r'(\d{4})', link)
        year_in_url = int(year_in_url.group(1))
        months_in_text = re.findall(
            r'(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)', lower_text)
        months_in_text = list(months_in_text)
        if oldest_known_year != year_in_url and len(months_in_text) == 0:
            oldest_known_month = ''
        elif oldest_known_year != year_in_url and len(months_in_text) > 0:
            for month in months_in_text:
                list_months = []
                month = months[month]
                list_months.append(month)
            oldest_known_month = list_months
        data['oldest_known_month'].append(oldest_known_month)
        print(f'Oldest known month: {oldest_known_month}')

        #
        # get OLDEST_KNOWN_DAY
        # retrieve the day from the url; when another day is found within the text, get that instead
        # unlike in oldest_known_year (more straightforward), we will list all days in the text if they're not the same as the one in the url
        #
        oldest_known_day = re.search(r'\d{4}\/\d{2}\/(\d{2})', link)
        oldest_known_day = str(oldest_known_day.group(1))
        if oldest_known_day in list(days.keys()):
            oldest_known_day = days[oldest_known_day]
        else:
            oldest_known_day = int(oldest_known_day)
        #
        # compare oldest_known_year to the year in the url.
        # if they're different (i.e. we derived the year from the text), we'll proceed with collecting days_in_text.
        #
        days_in_text = re.findall(r'(\d{1,2})\s+', lower_text)
        days_in_text = list(days_in_text)
        #
        # remove numbers that are invalid days of a month
        #
        for day in days_in_text:
            if int(day) > int(31):
                days_in_text.remove(day)
        if oldest_known_year != year_in_url and len(days_in_text) == 0:
            oldest_known_day = ''
        elif oldest_known_year != year_in_url and len(days_in_text) > 0:
            for day in days_in_text:
                list_days = []
                if day in list(days.keys()):
                    day = days[day]
                else:
                    day = int(day)
                list_days.append(day)
            oldest_known_day = list_days
        data['oldest_known_day'].append(oldest_known_day)
        print(f'Oldest known day: {oldest_known_day}')

        #
        # get OLDEST_KNOWN_SOURCE (null)
        #
        oldest_known_source = ''
        data['oldest_known_source'].append(oldest_known_source)
        print(f'Oldest known source: {oldest_known_source}')

        #
        # get DESC
        #
        desc = ''
        data['desc'].append(desc)
        print(f'Desc: {desc}\n')

        #
        # get DESC_LANGUAGE (null)
        # won't assume anything here for now because most of the descriptions I see are in Spanish, regardless of the region
        #
        desc_language = ''
        data['desc_language'].append(desc_language)
        print(f'Desc language: {desc_language}')

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
        # get VERIFIED_IN_MAPS (default to 0, will get 1 when it has OSM info)
        #
        if 'osm_info' in globals():
            verified_in_maps = 1
        else:
            verified_in_maps = 0
        data['verified_in_maps'].append(verified_in_maps)
        print(f'Verified in maps: {verified_in_maps}')

        #
        # get OPENSTREETMAP_LINK
        #
        try:
            openstreetmap_link = re.search(r'href="(.*?)"', osm_info)
            openstreetmap_link = f'https://www.openstreetmap.org{str(openstreetmap_link.group(1))}'
        except:
            openstreetmap_link = ''
        data['openstreetmap_link'].append(openstreetmap_link)
        print(f'OpenStreetMap link: {openstreetmap_link}')

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



# ------------------------------------------------------ #



### EXPORT THE DATA ###


# create a dataframe of all info collected
data_df = pd.DataFrame(data=data)
print('\nDataFrame created:\n')
print(data_df)

# export dataframe - xlsx supports unicode, so no more encoding fiascos compared to saving to csv
data_df.to_excel(f'countries/{country_en}.xlsx', index=False)



# ------------------------------------------------------ #


