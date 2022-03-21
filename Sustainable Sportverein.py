from bs4 import BeautifulSoup
import csv
import pandas as pd
import requests


source = requests.get('https://www.stadt-muenster.de/ms/opendata/belper.xml').text
immobilien = ["buergerhaus-kinderhaus", "hansa-berufskolleg", "stadthaus-2", "stadthaus-3", "stadtkasse-kaemmerei", "rathaus-stadtweinhaus", "standesamt", "gesundheits-und-veterinaeramt", "stadtbuecherei","buergerhaus-bennohaus", "aegidii-ludgeri-schule" , "albert-schweitzer-schule", "annette-von-droste-huelshoff-grundschule", "annette-von-droste-huelshoff-grundschule-nienberge", "astrid-lindgren-schule", "bodelschwinghschule", "davertschule", "dietrich-bonhoeffer-schule", "dreifaltigkeitsschule", "eichendorffschule-angelmodde", "gottfried-von-cappenberg-schule", "hermannschule", "idaschule", "idaschule2","johannisschule", "kardinal-von-galen-schule", "kinderhaus-west", "kreuzschule", "loevelingloh", "ludgerusschule-albachten","ludgerusschule-hiltrup","margaretenschule", "marienschule-hiltrup", "martin-luther-schule","martinischule", "matthias-claudius-schule","mauritzschule","melanchthonschule","michaelschule","mosaik-schule","norbertschule","overbergschule", "paul-gerhardt-schule", "paul-schneider-schule", "peter-wust-schule","pleisterschule","poetterhoekschule","primus-schule","grundschule-sprakel","theresienschule","thomas-morus-schule","wartburg-grundschule","adolph-kolping-berufskolleg","adolph-kolping-berufskolleg-2","adolph-kolping-berufskolleg-3","anne-frank-berufskolleg","annette-von-droste-huelshoff-gymnasium","augustin-wibbelt-schule","erna-de-vries-realschule","freiherr-vom-stein-gymnasium","friedensreich-hundertwasser-schule","geistschule","gesamtschule-muenster-mitte" , "geschwister-scholl-gymnasium", "paulinum","gymnasium-wolbeck","hans-boeckler-berufskolleg","hauptschule-coerde","johann-conrad-schlaun-gymnasium","ludwig-erhard-berufskolleg","mathilde-anneke-gesamtschule","pascal-gymnasium","ratsgymnasium","realschule-im-kreuzviertel","beckstrasse","richard-von-weizsaecker-schule","schillergymnasium","uppenbergschule","waldschule-kinderhaus","wilhelm-emmanuel-von-ketteler-berufskolleg","wilhelm-hittorf-gymnasium","kita-albachten","kita-am-edelbach","kita-inselbogen","kita-wolbeck","kita-berg-fidel","kita-brueningheide","kita-burgwall","kita-handorf","kinderhaus-west-1","kita-emmerbachtal","kita-gievenbeck","kita-in-der-alten-schule","kita-kinderhaus","kita-legdenweg","kita-loddengrund","kita-mecklenbeck","kita-normannenweg","kita-drostenhof","kita-am-gievenbach","kita-hiltrup-west","kita-im-moorhock","kita-killingstrasse","kita-rumphorst","kita-sonnentau","kita-wielerort","kita-wilkinghege","dreifachsportanlage","grosssporthalle-berg-fidel","sportanlage-hiltrup-sued","sportanlage-sentruper-hoehe","sporthalle-mosaik-schule","sporthalle-ost"]
immobilienadj = []
for i in immobilien:
    immobilienadj.append(i.title())
soup = BeautifulSoup(source, 'lxml')
alleSporthallen = []
for name in soup.findAll('name'):
    alleSporthallen.append(name.text.split(' ')[0])

Sporthallen = []
for i in alleSporthallen:
    for x in immobilienadj:
        if i == x:
            Sporthallen.append(i)


with open('Sporthallennutzung.csv', 'w', newline = '') as f:
    Header = ['Sporthalle', 'Wochentag', 'UhrzeitBeginn','UhrzeitEnde', 'Verein', 'Sportart']
    thewriter = csv.DictWriter(f, fieldnames=Header)
    thewriter.writeheader()

    for entry in soup.findAll()

print(Sporthallen)