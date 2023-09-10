# A Place for Salvador Allende

Non-exhaustive data and observations on how Salvador Allende, President of Chile from 1970 to 1973, is commemorated inside and outside Chile. This project is inspired by the _Una calle Salvador Allende_ website and made in time for the 50th anniversary of the coup d'état that marked Allende's death.

## About this project

This project builds up upon _Una calle Salvador Allende_ ("_A Salvador Allende street_") at <http://www.abacq.org/calle/>, a non-exhaustive resource for streets and other memorial places named after Salvador Allende, president of Chile from 1970 to 1973. The website accepted inputs from individuals around the world, mostly Chileans within and outside of Chile. The website was active from late 2000's (around the centennial of Allende's birth) to early 2010's, and many of these streets and places may have changed since then.

According to the website, there are at least [48 territories](texts/there_are_s_allende_streets_in.md) with a place for Salvador Allende. This project was able to confirm that he is present in at least 34 of them.

1. Algeria
2. Angola
3. Argentina
4. Australia
5. Austria
6. Belgium
7. Brazil
8. Canada
9. Chile
10. Colombia
11. Cuba
12. Denmark
13. Ecuador
14. El Salvador
15. France
16. Germany
17. Hungary
18. Italy
19. Luxembourg
20. Mexico
21. Mozambique
22. Netherlands
23. Nicaragua
24. Palestine
25. Peru
26. Portugal
27. Russia
28. Serbia
29. Slovakia
30. Spain
31. Turkey
32. United Kingdom
33. Uruguay
34. Venezuela

In a nutshell, this project goes through every article in _Una calle Salvador Allende_ and cross-checks them automatically using OpenStreetMap (OSM) and manually using Google Maps to see if they still exist. The scripts here automate most of the data collection, but the data are still manually verified whenever I have the time.

Of course, the website may have missed other places named after Salvador Allende. I originally planned to create a script that searches OSM for places named after Salvador Allende in every possible country and territory, but time, energy and legal constraints prevent me from doing this.

For now, this project focuses on the already extensive list of places in _Una calle Salvador Allende_. The file category ["Monuments and memorials to Salvador Allende"](https://commons.wikimedia.org/wiki/Category:Monuments_and_memorials_to_Salvador_Allende) at Wikimedia Commons also provides photos and information about some other memorial places.

Some articles in _Una calle Salvador Allende_ include places named after or dedicated to [Pablo Neruda](https://en.wikipedia.org/wiki/Pablo_Neruda), [Victor Jara](https://en.wikipedia.org/wiki/Victor_Jara), and other notable Chilean personalities. They are not included in this project but they are as interesting and relevant as Allende.

The main work for this project was done from March to September 2023, in time for the 50th anniversary of the [coup d'état where Allende died]((https://en.wikipedia.org/wiki/1973_Chilean_coup_d%27%C3%A9tat)).

## Technical notes on data collection

Test scripts and datasets are in my [datasets-of-interest](https://github.com/GoGroGlo/datasets-of-interest/tree/main/a-place-for-salvador-allende) repository. This repository contains the main dataset and scripts that have been tested to work. If there are discrepancies between the files in this repository and in datasets-of-interest, consider this repository as the more updated one.

The Python scripts used to scrape data can be found in the [**src**](src) folder of this repository. The way they were written may not be the best, but they fulfill the purpose of automating data collection in a way that is convenient for me.

The scripts take advantage of the semi-organized structure of each article in _Una calle Salvador Allende_ as explained below, but not all articles follow this structure so either a specific automated collection workflow or manual data collection had to be done for them. Documentation is available in the form of comments inside the scripts.

* The article URL usually has the format `http://www.abacq.org/calle/index.php?2011/06/27/527-san-joaquin-chile` with the year, month and date of posting followed by a random article number, the name of the locale, and the country where the memorial place is located. One article usually corresponds to one locale.
* Inside the article, the name of the locale is surrounded by `<strong>` HTML tags. This locale along with its country is then automatically verified using OpenStreetMap. For some articles containing multiple locales (hence multiple `<strong>` tags), the scraper iterates through each locale because some data are shared across them (e.g., country) while some others are distinct between them (e.g., name of memorial place).
* Descriptions present in the memorial place are surrounded by `<em>` HTML tags. These descriptions provide information about the memorial place, some of which (like the year, month and date of establishment) are also automatically scraped.

[allende_scraper_main.py](src/allende_scraper_main.py) is the generic script used to scrape data for most countries. This processes one country per run so that time between runs can be spaced. It relies on the webpage's [site map](http://www.abacq.org/calle/index.php?toc/toc) to retrieve country-specific links for scraping.

Some article contents have their own specific format that the generic script cannot process, hence separate scripts were made for [Portugal](src/allende_scraper_portugal.py) and [Liège in Belgium](src/allende_scraper_belgium_liege.py).

France has more than 300 memorial places to Allende that are presented across multiple articles in multiple formats.

* The [streets](src/allende_scraper_france_streets.py) were scraped first based on the list of street names, locales and postal codes provided in one article.
* Next, memorial places specifically in the [Île-de-France region](src/allende_scraper_france_paris.py) (referred to in its own article as the "Parisian region") were scraped to make sure they weren't already scraped in the first list of streets.
* Lastly, [all France articles](src/allende_scraper_france_links.py) in _Una calle Salvador Allende_ were checked to skip those that were already scraped in the first two lists, and added to the dataset when they haven't been.

All scripts generate a partial file of scraped data that is then manually verified to check for duplicates and missing or erroneous information. One memorial place can be featured in multiple articles in _Una calle Salvador Allende_, but the dataset only records one article link, usually the one that provides the most information. The partial files generated during my data collection period are available in the [**countries**](countries) folder. After verifying the data and clearing out the duplicates in the partial files, the final data were added to the main dataset.

### Disclaimer about web scraping

The scripts here rely on web scraping. While they are written so that they can run at a reasonably human pace, be aware that scraping too often may put a heavy strain on the website and may cause your IP address to be banned from the website. I recommend collecting country-specific data on spaced intervals that are long enough for websites to think you are a casual human browser rather than a bot.

## The dataset

The main dataset compiled by this project is available here: [**A Place for Salvador Allende: Raw Data**](a_place_for_salvador_allende_raw.xlsx).

### Important note

This is a **non-exhaustive** list of memorial places to Salvador Allende because there could be a lot more that are not available in _Una calle Salvador Allende_ and Wikimedia Commons, both of which relied on user submissions. Finding more memorial places available in online maps (without violating their terms of use and risking an IP address ban) requires more time and effort, and even then not all of these places are recorded in online maps in the first place.

Both automated and manual data collection are prone to errors, and although enough effort has been spent to minimize these errors, the correctness and completeness of every collected data cannot be guaranteed.

## Data dictionary

* `id` [int]
  * A distinct number that is assigned to a place when it is added to the main dataset `a_place_for_salvador_allende_raw.xlsx`. One ID corresponds to exactly one _standalone_ place.
  * _Standalone_ here means a distinct place that is located in a distinct locale and is established on a distinct date. For two or more places that are located in the same locale, each place is considered standalone if it can exist independently of the other.
    * Standalone example: If a street hypothetically changes its name from "Salvador Allende" to something else, but a park named after Salvador Allende would remain there, then both places are considered standalone (see IDs 146 and 147).
    * Non-standalone example: If there is a bus stop named after Salvador Allende, not because it deserves its own name but because the street it is located at is named "Salvador Allende", then the bus stop will not be added to the main dataset. For this reason, the hundreds of bus stops in Chile named after Salvador Allende are not included in the main dataset, but their corresponding streets are. Also, if there is a street named after Salvador Allende, but it is part of the passagaways around a park named after Salvador Allende, then only the park is included.
* `name` [str]
  * Either of the following:
    * The local name of the place (e.g., `Avenida Salvador Allende` or `Allendeho`); or
    * If the place is not explicitly named after Salvador Allende, the local name of the memorial itself (e.g., `L'Arc`) or the place where the memorial to Allende is located at (e.g., `Den Røde Plads`); or
    * If the place used to be named after Salvador Allende but has since changed its name, the current local name of the place (e.g., `бул. „Андрей Сахаров“ / Boulevard "Andrej Sakharov"`); or
    * If no local name is available, a short description of the place (e.g., `Salvador Allende memorial tree and plate`).
* `type` [str]
  * The type of establishment of the place, normalized in this dataset to group together similar establishments.
* `region` [str]
  * The continent or part thereof where the country is located.
* `country` [str]
  * The country where the place is located, specified either by <http://www.abacq.org/calle/> or OpenStreetMap.
* `locale_1` [str]
  * The topmost geographical unit of the country, for example a Chilean region, Canadian province, or French overseas department (Réunion, French Guiana). This is the only locale column that is always populated.
* `locale_2` [str, optional]
  * The second topmost geographical unit of the country, used for distinguishing between places within the same country and for getting more specific within `locale_1`.
* `locale_3` [str, optional]
  * The third most localized geographical unit of the country, used for distinguishing between places within the same country. Could be anything from a city to a park to a specific street.
* `locale_4` [str, optional]
  * The second most localized geographical unit of the country, used for distinguishing between places within the same country. Could be anything from a city to a park to a specific street.
* `locale_5` [str, optional]
  * The most localized geographical unit of the country, used for distinguishing between places within the same country. Could be anything from a city to a park to a specific street.
* `zip_code` [str, optional]
  * The postal code of the locale, if available.
* `latitude` [int, optional]
  * The first number and horizontal axis of the map coordinates of the locale (e.g., -33.44202926, -70.65339974), where a positive latitude corresponds to north of the equator and a negative latitude corresponds to south of the equator.
* `longitude` [int, optional]
  * The second number and vertical axis of the map coordinates of the locale (e.g., -33.44202926, -70.65339974), where a positive longitude corresponds to east of the prime meridian and a negative longitude corresponds to west of the prime meridian.
* `oldest_known_year` [int, optional]
  * Either of the following:
    * The year in which the place is established; or
    * The year in which the place is explicitly named after Salvador Allende, if it was established with a previous name; or
    * The oldest year in which the place is known to exist _and_ to be named after Salvador Allende; or
    * Null if any of the above is unknown.
  * Sometimes a place would be officially reinaugurated or remodeled, but it has been attested in <http://www.abacq.org/calle/> to exist earlier with Allende's name. In these cases, the oldest known year of existence is recorded (see IDs 165 and 173).
* `oldest_known_month` [int, optional]
  * If known, a number from 1 to 12 corresponding to the month that goes with the `oldest_known_year`. Null if unknown.
* `oldest_known_day` [int, optional]
  * If known, a number from 1 to 31 corresponding to the day that goes with the `oldest_known_year`. Null if unknown. A full date can be derived if `oldest_known_year`, `oldest_known_month` and `oldest_known_day` are known.
* `oldest_known_source` [str, optional]
  * Populated only if `oldest_known_year` is known and can be either of the following:
    * `desc place` - The date of establishment of the place is explicitly stated within the place's `desc`.
    * `desc abacq` - The date of establishment of the place comes from contributors at <http://www.abacq.org/calle/>.
    * `desc implied` - The date of establishment of the place is derived from another nearby place whose date of establishment is known.
    * `desc other` - The date of establishment of the place is derived from other sources, usually the contents of file category ["Monuments and memorials to Salvador Allende"](https://commons.wikimedia.org/wiki/Category:Monuments_and_memorials_to_Salvador_Allende) at Wikimedia Commons.
    * `abacq date posted` - The date in which the place was first featured in an article in <http://www.abacq.org/calle/>.
    * `openstreetmap` - The date in which the place was first edited in OpenStreetMap to exist and/or be named after Salvador Allende.
    * `google maps` - The earliest date in which Google Maps street view imagery reveals that the place exists and/or is named after Salvador Allende.
  * If `oldest_known_source` begins with `desc`, then the `oldest_known_year`, `oldest_known_month` and/or `oldest_known_day` is fairly reliable. This avoids a certain data bias where a lot of places are first recorded on the internet during certain years when they in fact have existed way before the internet era.
* `desc` [str, optional]
  * Any text that is written within the place (e.g., on street signs, memorial plates, and monument inscriptions). If the text cannot be reliably transcribed in its native language, we take its translation as provided in the `abacq_reference` article. Null if original text cannot be reliably transcribed and no translation is available.
* `desc_language` [str, optional]
  * If `desc` is present in the place itself (regardless of whether it can be reliably transcribed), this is the [two-letter ISO code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) of the native language in which the `desc` is written.
* `alt_name` [str, optional]
  * Alternative name for the place, if known. If the place has a different name, but it is not known whether it is a former name, then the name is populated here.
* `former_name` [str, optional]
  * Former name of the place, if known. If the place was once named after Salvador Allende but has since changed its name, the name with Salvador Allende is populated here.
* `verified_in_maps` [int]
  * `1` if the place is verified to be present in OpenStreetMap and/or Google Maps, otherwise `0`. Good for filtering places that are verified to exist.
* `openstreetmap_link` [str, optional]
  * The link to the OpenStreetMap listing of the place, if `verified_in_maps` = `1`. Good for viewing the listing's edit history.
* `google_maps_link` [str, optional]
  * The link to the Google Maps listing of the place, if `verified_in_maps` = `1`. Good for viewing current and historical street views, if available.
* `abacq_reference` [str, optional]
  * The link to an article from <http://www.abacq.org/calle/> about the place. Although there can be more than one article for the same place, this column only accommodates one link per place. Refer to the webpage's [site map](http://www.abacq.org/calle/index.php?toc/toc) for a full list of articles.

## Data investigation summary

My full investigation is available here: [**A Place for Salvador Allende: A Data Investigation**](a_place_for_salvador_allende.md).

_In case of discrepancy between this excerpt and the data investigation page, consider the data investigation page the more current one._

This project was able to gather from _Una calle Salvador Allende_, Wikimedia Commons, map websites and others a total of 780 memorial places around the world, but the project makes a distinction between extant and non-extant places. Here, a place is extant if `former_name` does not contain `Allende` and if `verified_in_maps` = `1`. There are 729 extant places that meet this criteria.

This project was able to prove using hundreds of memorial places that [Dr. Salvador Allende Gossens](texts/salvador_allende_gossens_memoria_chilena_en.md), President of Chile from 1970 until his overthrow and death on 11 September 1973, is more commemorated _outside_ Chile than _inside_ Chile. The story does not end here, though.

⚠ **Content warning: the following paragraph contains references to state-sponsored mass violence.**

The lack of memorials to Allende inside Chile from 1973 to 1990 is due to the active repression of memory done by the military dictatorship after overthrowing Allende in a violent coup d'état. Aside from refusing to organize a state funeral for Allende like any other deceased president deserves, the military dictatorship also systematically imprisoned, tortured, killed and forced into disapperance a lot of people in Chile who could have given the posthumous respects to Allende that the dictatorship refused to give.

Chileans who were in a capacity to give posthumous respects to Allende had to escape the repression in their country to be able to do so. From their respective places of exile outside Chile, they were able to find solidarity among fellow Chileans and other locals who sympathized with Allende's peaceful, democratic efforts towards socialism and social justice, and at the same time condemned the violence committed by the dictatorship beginning from the day they overthrew Allende's government.

Before the 1973 coup, Allende's government saw itself under the global political context of a competition between capitalist interests represented by the United States and its allies, and socialist interests represented by the Soviet Union and its allies. The United States saw the socialist tendency of Allende's government as a threat to its interests, hence it supported all possible means to destabilize and overthrow it, up to and including the coup. However, the US government failed to disassociate Allende's democratic path towards socialism from the violent means of gaining and maintaining power that the Soviet Union and its allies were notorious for.

The differences in means (violent vs. democratic) did not prevent some foreign socialist governments from commemorating the Chilean president who pursued the same socialist goals. Foreign governments which profess democratic values have been glad to commemorate him, foreign _socialist_ governments which profess democratic values doubly so. This, combined with solidarity by, among and towards the Chilean community, led to the creation of memorial spaces to Salvador Allende practically everywhere in the world except Chile.

The military dictatorship in Chile ended in 1990, and memorial places to Allende in his own country were starting to be established despite resistance from political detractors (who even resisted against his long overdue state funeral). Elsewhere, efforts to commemorate him continued. The number of new memorial spaces and commemorative events inside and outside Chile peaked in 2008, Allende's 100th birth anniversary. The other peak happened in 1973, right after the coup d'état and Allende's death, and as expected all memorial places to Allende at that time were established outside Chile.

Memorial places to Allende typically represent him as a victim or martyr who died for the sake of democracy and/or socialism and/or social justice in the face of absolute violence supported by Chilean and foreign interest groups who want to reclaim their privileges from the Chilean public to themselves. Many of these places quote from his [final speech]((https://www.marxists.org/archive/allende/1973/september/11.htm)) to the public on the day of the coup, which was an impactful proof of his active defiance against the coup and his commitment towards the people who had elected him as president.

Even though some details about Allende are uncertain, such as how exactly he died, and memorial places tend to contradict each other in these details, this project can conclude with certainty that memorial places to Salvador Allende are scattered around the world due to efforts from socialists, democrats and Chileans, and yet they managed to paint a cohesive image of how he would have wanted to be remembered after saying his last words.

> Workers of my country: I want to thank you for the loyalty that you always had, the confidence that you deposited in a man who was only an interpreter of great yearnings for justice, who gave his word that he would respect the Constitution and the law and did just that.
>
> _—Excerpt from Salvador Allende's last speech, 11 September 1973_

## My motivation for doing this

![An edited screenshot of a tweet from Gabriel Boric, current president of Chile - edited text follows.](assets/GabrielBoric_a_estas_alturas.png)

> At this point, politically it doesn't really matter how Allende died (if historical%). What matters is that we have streets and squares named after him.
>
> _—Gabriel Boric, current president of Chile. [Tweet](https://twitter.com/GabrielBoric/status/75411227647545344) from 31 May 2011, but edited and taken out of context._

Full disclosure: I am not from Chile, I am not of Chilean descent, and I do not have any material connections with Chile.

However, I became interested in Chile because I used to be a data analyst collecting data about publicly traded companies in Latin America. I also have a degree related to social sciences, which informs my approach towards this data investigation.

_Story time:_ Back when I was in my first year at university, a Chilean professor visited and gave a lecture on Chilean and Southeast Asian relations. I tried to take notes, but my academic interest at that time was clearly not Chilean affairs, so my notes ended up half-baked and I wrote the most controversial statement of 2015:

> Stable democracy (had an authoritarian gov't from 1960s to 1973)

A few years later, I finished university and got a job as a data analyst where one of the markets that we were collecting data about on is... Chile, so this time I had to be involved in Chilean affairs. During that time, I learned enough Spanish to be able to read it with minimal machine translation (I am not a fluent speaker, though).

Then the COVID pandemic came and instead of exploring the central business district around my workplace I had to stay at home. I had nothing much to do aside from reading random Wikipedia articles and getting myself into Wikipedia rabbit holes, which included articles on the history of Chile.

That's how I found out six years later that Chile, in fact, did _not_ have an authoritarian government from the 1960s to 1973. I got the years mixed up because there indeed was an authoritarian government after 1973, but before that the presidents were democratically elected. This included Salvador Allende, the last democratically elected president before 1973.

My social sciences-educated self genuinely appreciates all the efforts that the Chilean diaspora and their counterparts back home have made to keep Allende's memory alive despite active suppression from the authoritarian government and their allies. I've never seen a memorial effort as scattered yet cohesive as this one.

This project is my penance for perpetuating the sin of suggesting that Salvador Allende was authoritarian. Kidding aside, Chile's rough history from Allende onwards was something I didn't have notes of back in 2015 and which I had to find out myself several years later. I am not an expert on the matter; I am just someone who is interested in it and would like to contribute to making this narrative more known outside Chile, to the best of my understanding and abilities.

⚠ **Content warning: the following two paragraphs contain references to suicide.**

I did say that I am not from Chile, I am not of Chilean descent, and I do not have any material connections with Chile. However, I still do have a personal connection towards Allende as a topic.

I got interested enough in the topic to be aware of the details of how Allende died, at least according to the 2011 autopsy. And then I spent a year (perhaps more) fighting my own suicidal thoughts. I eventually got therapy for them, and I decided that engaging further with someone who once [shared](https://www.nytimes.com/1973/09/12/archives/socialist-says-allendeonce-spoke-of-suicide.html)  his own suicidal thoughts two years before doing the act is enabling my own suicidal thoughts, so I dropped all my interest towards Allende and Chile at large for a while. If Allende was actually assassinated and no one disputed it, I wouldn't have needed to write this whole paragraph.

I planned to visit Chile during the 50th anniversary of the coup d'état so that I can participate in the commemorations, but I ended up deciding that the money for the trip is better spent on physically and professionally improving myself as a form of mental health recovery. I only started this project when I felt that I was mentally prepared to go back to this interest—and here I am collecting all these streets, squares and spaces for Salvador Allende while adding concrete examples of my professional skillset, understanding further why Allende is worth commemorating, and making sense of my thoughts about these topics.

I made this project mostly for myself (I personaly think of this as a mini-thesis that I would've made if I were studying at the moment), but I would be glad if someone else finds this useful. This project was completed in time for the 50th anniversary of the coup d'état and might get updates from time to time—I do hope that my next updates will be due to new memorial places to Allende.

_¡Allende vive!_

_Un abrazo_ and warm regards,

Glo (they/them)

September 2023

## License

Glo ([@GoGroGlo](https://GoGroGlo.carrd.co)) maintains this project. The datasets and texts in this project are licensed under the [Creative Commons Attribution 4.0 International license](https://creativecommons.org/licenses/by/4.0/), and the underlying source code used to collect data is licensed under the [MIT license](MIT_License.txt). The datasets, texts, and source code can be used for any purpose (hopefully constructive) as long as credit is given—it can be something as simple as a link to this page (<https://github.com/GoGroGlo/a-place-for-salvador-allende>).
