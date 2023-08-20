# A Place for Salvador Allende

Mapping (almost) every place in the world named after the Chilean president, inspired by the _Una calle Salvador Allende_ website.

## About this project

This project builds up upon _Una calle Salvador Allende_ at <http://www.abacq.org/calle/>, which compiled every street and every place named after Salvador Allende, president of Chile from 1970 to 1973. The website accepted inputs from individuals around the world, mostly Chileans within and outside of Chile. The website was active from late 2000's (around the centennial of Allende's birth) to early 2010's, and many of these streets and places may have changed since then.

According to the website, there are at least 48 territories with a place for Salvador Allende:

1. Angola
2. Algeria
3. Argentina
4. Australia
5. Austria
6. Belgium
7. Bosnia and Herzegovina
8. Brazil
9. Bulgaria
10. Canada
11. Chile
12. Colombia
13. Cuba
14. Czechia
15. Denmark
16. Dominican Republic
17. Ecuador
18. El Salvador
19. France
20. Germany
21. Guinea-Bissau
22. Hungary
23. India
24. Iran
25. Israel
26. Italy
27. Luxembourg
28. Mexico
29. Mozambique
30. Netherlands
31. Nicaragua
32. North Macedonia
33. Pakistan
34. Palestine
35. Paraguay
36. Peru
37. Portugal
38. Republic of the Congo
39. Russia
40. Saudi Arabia
41. Serbia
42. Slovakia
43. Spain
44. Turkey
45. United Kingdom
46. United States
47. Uruguay
48. Venezuela

In a nutshell, this project goes through every article in <http://www.abacq.org/calle/> and cross-checks them automatically using OpenStreetMap (OSM) and manually using Google Maps to see if they still exist. The scripts here automate most of the data collection, but the data is still manually verified whenever I have the time. Every place is kept in a .xlsx file for reference and investigation of anyone interested in this dataset.

Of course, the website may have missed other places named after Salvador Allende. I plan to create a script that searches OSM for places named after Salvador Allende in every possible country and territory, but this will come later on. For now, this project focuses on the already extensive list of places in <http://www.abacq.org/calle/>.

Some articles include places named after or dedicated to Pablo Neruda, Victor Jara, and other notable Chilean personalities; they are not included in this project.

**This project is a work in progress**, and it will only contain complete datasets and scripts that have been tested to work. Test scripts and datasets are in my [datasets-of-interest](https://github.com/GoGroGlo/datasets-of-interest/tree/main/a-place-for-salvador-allende) repository.

My data investigation (also a work in progress) can be found here: [**A Place for Salvador Allende: A Data Investigation**](a_place_for_salvador_allende.md).

## Data dictionary

* `id`
  * [int] A distinct number that is assigned to a place when it is added to the main dataset `a_place_for_salvador_allende.xlsx`. One ID corresponds to exactly one _standalone_ place.
  * _Standalone_ here means a distinct place that is located in a distinct locale and is established on a distinct date. For two or more places that are located in the same locale, each place is considered standalone if it can exist independently of the other.
    * Standalone example: If a street changes its name from "Salvador Allende" to something else, but a park named after Salvador Allende remains there, then both places are considered standalone (see IDs 146 and 147).
    * Non-standalone example: If there is a bus stop named after Salvador Allende, not because it deserves its own name but because the street it is located at is named "Salvador Allende", then the bus stop will not be added to the main dataset. For this reason, the hundreds of bus stops in Chile named after Salvador Allende are not included in the main dataset, but their corresponding streets are. Also, if there is a street named after Salvador Allende, but it is part of the passagaways around a park named after Salvador Allende, then only the park is included.
* `name`
  * [str] Either of the following:
    * The local name of the place (e.g., `Avenida Salvador Allende` or `Allendeho`); or
    * If the place is not explicitly named after Salvador Allende, the local name of the memorial itself (e.g., `L'Arc`) or the place where the memorial to Allende is located at (e.g., `Den Røde Plads`); or
    * If the place used to be named after Salvador Allende but has since changed its name, the current local name of the place (e.g., `бул. „Андрей Сахаров“ / Boulevard "Andrej Sakharov"`); or
    * If no local name is available, a short description of the place (e.g., `Salvador Allende memorial tree and plate`).
* `type`
  * [str] The type of establishment of the place, normalized to group together similar establishments.
* `region`
  * [str] The continent or part thereof where the country is located.
* `country`
  * [str] The country where the place is located, specified either by <http://www.abacq.org/calle/> or OpenStreetMap.
* `locale_1`
  * [str] The topmost geographical unit of the country, for example a US state, Canadian province, or French overseas territory (Réunion, French Guiana). This is the only locale column that is always populated.
* `locale_2`
  * [str, optional] The second topmost geographical unit of the country, used for distinguishing between places within the same country and for getting more specific within locale_1.
* `locale_3`
  * [str, optional] The third most localized geographical unit of the country, used for distinguishing between places within the same country. Could be anything from a city to a park to a specific street.
* `locale_4`
  * [str, optional] The second most localized geographical unit of the country, used for distinguishing between places within the same country. Could be anything from a city to a park to a specific street.
* `locale_5`
  * [str, optional] The most localized geographical unit of the country, used for distinguishing between places within the same country. Could be anything from a city to a park to a specific street.
* `zip_code`
  * [str, optional] The postal code of the locale, if available.
* `latitude`
  * [int, optional] The first number and horizontal axis of the map coordinates of the locale (e.g., -33.44202926, -70.65339974), where a positive latitude corresponds to north of the equator and a negative latitude corresponds to south of the equator.
* `longitude`
  * [int, optional] The second number and vertical axis of the map coordinates of the locale (e.g., -33.44202926, -70.65339974), where a positive longitude corresponds to east of the prime meridian and a negative longitude corresponds to west of the prime meridian.
* `oldest_known_year`
  * [int, optional] Either of the following:
    * The year in which the place is established; or
    * The year in which the place is explicitly named after Salvador Allende, if it was established with a previous name; or
    * The oldest year in which the place is known to exist _and_ to be named after Salvador Allende; or
    * Null if any of the above is unknown.
  * Sometimes a place would be officially reinaugurated or remodeled, but it has been attested in <http://www.abacq.org/calle/> to exist earlier with Allende's namw. In these cases, the oldest known year of existence is recorded (see IDs 165 and 173).
* `oldest_known_month`
  * [int, optional] If known, A number from 1 to 12 corresponding to the month that goes with the `oldest_known_year`. Null if unknown.
* `oldest_known_day`
  * [int, optional] If known, A numnber from 1 to 31 corresponding to the day that goes with the `oldest_known_year`. Null if unknown. A full date can be derived if `oldest_known_year`, `oldest_known_month` and `oldest_known_day` are known.
* `oldest_known_source`
  * [str, optional] Populated only if `oldest_known_year` is known and can be either of the following:
    * `desc place` - The date of establishment of the place is explicitly stated within the place's `desc`.
    * `desc abacq` - The date of establishment of the place comes from contributors at <http://www.abacq.org/calle/>.
    * `desc implied` - The date of establishment of the place is derived from another nearby place whose date of establishment is known.
    * `desc other` - The date of establishment of the place is derived from other sources, usually the contents of file category ["Monuments and memorials to Salvador Allende"](https://commons.wikimedia.org/wiki/Category:Monuments_and_memorials_to_Salvador_Allende) at Wikimedia Commons.
    * `abacq date posted` - The date in which the place was first featured in an article in <http://www.abacq.org/calle/>.
    * `openstreetmap` - The date in which the place was first edited in OpenStreetMap to exist and/or be named after Salvador Allende.
    * `google maps` - The earliest date in which Google Maps street view imagery reveals that the place exists and/or is named after Salvador Allende.
  * If `oldest_known_source` begins with `desc`, then the `oldest_known_year`, `oldest_known_month` and/or `oldest_known_day` is fairly reliable. This avoids a certain data bias where a lot of places are first recorded on the internet during certain years when they in fact have existed way before the internet era.
* `desc`
  * [str, optional] Any text that is written within the place (e.g., on street signs, memorial plates, and monument inscriptions). If the text cannot be reliably transcribed in its native language, we take its translation as provided in the `abacq_reference` article. Null if original text cannot be reliably transcribed and no translation is available.
* `desc_language`
  * [str, optional] If `desc` is present, this is the [two-letter ISO code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) of the native language in which the `desc` is written.
* `alt_name`
  * [str, optional] Alternative name for the place, if known. If the place has a different name, but it is not known whether it is a former name, then the name is populated here.
* `former_name`
  * [str, optional] Former name of the place, if known. If the place was once named after Salvador Allende but has since changed its name, the name with Salvador Allende is populated here.
* `verified_in_maps`
  * [int] `1` if the place is verified to be present in OpenStreetMap and/or Google Maps, otherwise `0`. Good for filtering places that are verified to exist.
* `openstreetmap_link`
  * [str, optional] The link to the OpenStreetMap listing of the place, if `verified_in_maps` is `1`. Good for viewing the listing's edit history.
* `google_maps_link`
  * [str, optional] The link to the Google Maps listing of the place, if `verified_in_maps` is `1`. Good for viewing current and historical street views, if available.
* `abacq_reference`
  * [str, optional] The link to an article from <http://www.abacq.org/calle/> about the place. Although there can be more than one article for the same place, this column only accommodates one link per place. Refer to the webpage's [site map](http://www.abacq.org/calle/index.php?toc/toc) for a full list of articles.

## Disclaimer about web scraping

The scripts here rely on web scraping. While they are written so that they can run at a reasonably human pace, be aware that scraping too often may put a heavy strain on the website and may cause your IP address to be banned from the website. I recommend collecting country-specific data on spaced intervals that are long enough for websites to think you are a casual human browser rather than a bot.

## License

[GoGroGlo](https://GoGroGlo.carrd.co) maintains this project. The datasets and texts in this project are licensed under the [Creative Commons Attribution 4.0 International license](https://creativecommons.org/licenses/by/4.0/), and the underlying source code used to collect data is licensed under the [MIT license](MIT_License.txt). The datasets, texts, and source code can be used for any purpose (hopefully constructive) as long as credit is given—it can be something as simple as a link to this page.
