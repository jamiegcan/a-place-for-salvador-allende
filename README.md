# A Place for Salvador Allende

Mapping (almost) every place in the world named after the Chilean president, inspired by the "Una calle Salvador Allende" website.

## About this project

This project builds up upon "Una calle Salvador Allende" at http://www.abacq.org/calle/, which compiled every street ("una calle") and every place named after Salvador Allende, president of Chile from 1970 to 1973. The website accepted inputs from individuals around the world, mostly Chileans within and outside of Chile. The website was active from late 2000's (centennial of Allende's birth) to early 2010's, and many of these streets and places may have changed since then.

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

In a nutshell, this project goes through every article in http://www.abacq.org/calle/ and cross-checks them using OpenStreetMap (OSM) and Google Maps to see if they still exist. The scripts here automate most of the data collection, but the data is still manually verified whenever I have the time. Every place is kept in a table for reference and investigation of anyone interested in this dataset.

Of course, the website may have missed other places named after Salvador Allende. I plan to create a script that searches OSM for places named after Salvador Allende (or Salvador Allende Gossens, "Gossens" being the second surname) in every possible country and territory, but this will come later on. For now, this project focuses on the already extensive list of places in the website.

**This repo is a work in progress**, but it will only contain complete data tables and scripts that have been tested to work. Test scripts and data tables are in my [datasets-of-interest](https://github.com/GoGroGlo/datasets-of-interest) repo.

## Disclaimer

The scripts here rely on web scraping. If you're going to run the scripts, be aware that scraping too often may put a heavy strain on the website and may cause your IP address to be banned from the website. I recommend collecting country-specific data on spaced intervals that are long enough for websites to think you are a casual human browser rather a bot. I also recommend waiting for a few minutes between web scrapes - I do it by delaying my response in every user input.

> Script: `>>> Please enter one of the countries above: `
> 
> Me: \*goes out for some snacks and drinks, then returns to my desk to respond to the script\*

## This repository is in the public domain to encourage open and replicable data

The data that are collected in this repo are available for anyone for any positive purpose. The scripts here can also be adapted for any positive purpose, including data collection of places named after anyone or anything. 



# Why are there more places named after Salvador Allende that are outside of Chile than inside Chile? A data investigation [work in progress]

## Who was Salvador Allende?

**Content warning: this section contains references to suicide.**

[Wikipedia's summary of Allende's life](https://en.wikipedia.org/wiki/Salvador_Allende) provides enough information without causing information overload, and I'll paste it here for everyone's convenience:

> Salvador Guillermo Allende Gossens (26 June 1908 – 11 September 1973) was a Chilean physician and socialist politician who served as the 28th president of Chile from 3 November 1970 until his death on 11 September 1973. He was the first Marxist to be elected president in a liberal democracy in Latin America.
> 
> Allende's involvement in Chilean politics spanned a period of nearly forty years, having covered the posts of senator, deputy and cabinet minister. As a life-long committed member of the Socialist Party of Chile, whose foundation he had actively contributed to, he unsuccessfully ran for the national presidency in the 1952, 1958, and 1964 elections. In 1970, he won the presidency as the candidate of the Popular Unity coalition, in a close three-way race. He was elected in a run-off by Congress, as no candidate had gained a majority.
> 
> As president, Allende sought to nationalize major industries, expand education and improve the living standards of the working class. He clashed with the right-wing parties that controlled Congress and with the judiciary. On 11 September 1973, the military moved to oust Allende in a coup d'état supported by the United States Central Intelligence Agency (CIA). As troops surrounded La Moneda Palace, he gave his last speech vowing not to resign. Later that day, Allende died by suicide in his office.
> 
> Following Allende's death, General Augusto Pinochet refused to return authority to a civilian government, and Chile was later ruled by a military junta until 1990, ending more than four decades of uninterrupted democratic governance. The military junta that took over dissolved the Congress of Chile, suspended the Constitution, and began a program of persecuting alleged dissidents, in which at least 3,095 civilians disappeared or were killed.

The [Simple English version](https://simple.wikipedia.org/wiki/Salvador_Allende) of Wikipedia's article on Allende works as a more accessible version of the full English Wikipedia article, especially for those who are new to socialist discourse. Pardon this article's occasional repetitiveness to the point of being absurd because apparently "_some feel that he took his own life by committing suicide_".

## Why are places named after Salvador Allende?

When we talk about Salvador Allende, two things matter the most: _socialist_ and _democratically elected_. These two explain a lot about his presence around the world.

* Allende has been a socialist since his student days. As a socialist, he believed that the gap between the richest and the poorest people in Chile is unacceptable and this could be eliminated when resources and institutions are owned by the Chilean state rather than the private sector who also happen to be the richest people. He campaigned for the improvement of the lives of working-class people, and for that he got the support of a lot of them.
* Socialists around the world have their vocal (and wealthy) opponents, and Chilean socialists like Allende were no exception. This is why Allende had a hard time winning the presidential elections the first three times he tried. Back then, socialists became leaders of their own countries not through elections but through chaotic revolutions. Allende was convinced that he could avoid another chaotic revolution, so he ran again for the presidency in 1970. This time, he became the first democratically elected socialist leader in the world. When he became president, he established and maintained contact with other socialist leaders around the world who recognized that Allende was seeking the same goals as them (socialism) through different means (peaceful democratic processes).

Allende's presidency, which started peacefully in 1970, ended violently with the coup in 1973 that was led by Augusto Pinochet. The military leadership took over the country and refused to give him a state funeral that every president who dies in office deserves. A lot of Chileans, especially Allende's supporters, had to seek exile abroad to save themselves from the human rights violations done by Pinochet's military dictatorship. Allende effectively became a taboo topic during the dictatorship, and virtually no one in Chile was able to pay respects to the late president because they either had to escape from Chile or was already killed by the army.

Outside of Chile, I can identify three interest groups that have been naming and building things in honor of Salvador Allende:
* Chilean diaspora
    * These individuals appreciate Allende for defending the Chilean working class throughout his political career, and of course for having been President of the Republic of Chile (arguably the most widely known, if not controversial, president of Chile).
    * When the Chilean state under Pinochet won't do the necessary honors for Allende, these Chileans will, from their respective countries of residence.
* Socialists (regardless of whether they gained power through democratic means)
    * These individuals appreciate Allende for being a socialist who never softened his position despite fierce opposition.
    * Some socialist leaders have named and built places in honor of Allende and portrayed him as a martyr to further their own socialist agenda - see Cuba for example.
* Advocates of democracy (regardless of whether they're outwardly socialist or not)
    * These individuals appreciate Allende for believing in democratic institutions until the end.

Inside Chile, Allende only got the historical recognition he deserved (including a state funeral) with the return of democracy in 1990.

This part would benefit from specific examples and we'll get there once we've scraped the web for those places.

## How did Salvador Allende die, really?

**Content warning: this section contains references to suicide and murder.**

You may have read that Allende "_took his own life by committing suicide_", but some monuments, plates and street signs say that he was killed by the coup plotters. 

Allende himself hinted in his speech during the coup that this was going to be his last, and that he would be willing to sacrifice himself, though the manner of sacrifice was vague.

> Given these facts, the only thing left for me is to say to workers: I am not going to resign! Placed in a historic transition, I will pay for the loyalty of the people with my life.
> 
> Long live Chile! Long live the people! Long live the workers! These are my last words, and I am certain that my sacrifice will not be in vain.

Wikipedia's article on the [death of Salvador Allende](https://en.wikipedia.org/wiki/Death_of_Salvador_Allende) briefly explains the controversy and why Allende would be more inclined to kill himself instead of getting killed:

> Isabel Allende Bussi, the daughter of Salvador Allende and a former member of the Senate of Chile, stated that the Allende family had long accepted that the former president shot himself. She told the BBC, "The report conclusions [that Allende died by suicide] are consistent with what we already believed. When faced with extreme circumstances, he made the decision of taking his own life, instead of being humiliated."
> 
> Carlos Altamirano, who was close to Allende, recalls that prior to the coup, Allende would have dismissed his suggestion to seek refuge in a loyalist regiment and fight back from there. In Altamirano's words Allende also rejected the option "to do as so many dictators and presidents of Latin America, that is to grab a briefcase full of money and take a plane out the country." Allende was an admirer of José Manuel Balmaceda, a Chilean president who died by suicide in face of his defeat in the Chilean Civil War of 1891. According to Altamirano, Allende was "obsessed with the attitude of Balmaceda."

However, I think there are several reasons a lot of individuals found it easier to believe that Allende was murdered.
* The first people who announced that Allende had killed himself were the coup plotters. Why would Allende's supporters believe what their enemies are saying?
    * An actual exchange between Pinochet and Vice Admiral Patricio Carvajal during the coup - 05:19 onwards in this [video from Memoria Chilena](http://www.memoriachilena.gob.cl/archivos2/videos/MC0043416.mpg):
        * Carvajal: [_in Spanish_] There is a communication from the infantry school staff who is already inside La Moneda, and due to the possibility of interception I will transmit it in English: [_in English, verbatim_] They say that Allende committed suicide and is dead now. [_in Spanish_] Tell me if you understood.
        * Pinochet: [_in Spanish_] Understood, perfectly understood. 
* Suicide can be interpreted as an acceptance of defeat and is highly contradictory to Allende's announcement in his last speech that he would not resign. Supporters would rather believe that Allende fought until the end.
* The exact method of Allende's suicide, which was only confirmed many years after the event, can come off as ridiculous or made-up to some individuals. 
    * Who else would shoot oneself with an AK-47? Which was held between the legs and under the chin? And which was a gift from none other than Fidel Castro of Cuba? This is too oddly specific. Allende being shot by enemies would be much easier to imagine, I suppose.

Anecdotal evidence supporting suicide only came about after 1990, and an autopsy in 2011 confirmed it. Until then, Allende's supporters and others could only speculate about how he died, and the easiest reason was death in the hands of the enemies.

Right now, does believing that Allende died in his own hands make someone anti-Allende and pro-coup? Not necessarily, according to some witnesses of his death: 

> The other witnesses kept silent until after the restoration of democracy in Chile, as they believed (according to their own statements) that to corroborate the version of a suicide would in some measure downgrade Allende's sacrifice and lend support to the military regime.

With that said, it would be interesting to know which places claim murder and if any place ever acknowledged Allende's conscious, free-willed decision on that fateful day. We can create a new column which classifies each place's stance on Allende's death:
* null  -   The place doesn't mention Allende's death
* -1    -   Explicitly mentions that Allende was murdered
* -0.5  -   Mentions Allende's death in a vague way, but suggests murder
* 0     -   Mentions Allende's death, but suggests neither murder nor suicide
* 0.5   -   Mentions Allende's death in a vague way, but suggests suicide
* 1     -   Explicitly mentions that Allende died by suicide

`desc` could be helpful here, but not every data row comes with one so this requires manual verification.

