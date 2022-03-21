from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup
import datetime
from datetime import date, timedelta
import csv

#Frühester Beginn der Aufzeichnung 2015 Dezember nach erstem Skim, sinnvoll vielleicht nur die letzten 2-3 Jahre?
a = datetime.datetime.today()

numdays = 50
dateList = []
for x in range (0, numdays):
    dateList.append(a - datetime.timedelta(days = x))

adjDateList = []
for x in range (0, numdays):
    adjDateList.append(dateList[x].strftime('%d').lstrip('0') + '.' + dateList[x].strftime('%m').strip('0') + '.' + dateList[x].strftime('%y'))
b = adjDateList[1]

with open('Energiedaten.csv', 'w', newline = '') as f:
    Header = ['Immobilie', 'Datum', 'Energietyp', 'Verbrauch']
    thewriter = csv.DictWriter(f, fieldnames=Header)
    thewriter.writeheader()

immobilien = ["buergerhaus-kinderhaus", "stadthaus-2", "stadthaus-3", "stadtkasse-kaemmerei", "rathaus-stadtweinhaus", "standesamt", "gesundheits-und-veterinaeramt", "stadtbuecherei","buergerhaus-bennohaus", "aegidii-ludgeri-schule" , "albert-schweitzer-schule", "annette-von-droste-huelshoff-grundschule", "annette-von-droste-huelshoff-grundschule-nienberge", "astrid-lindgren-schule", "bodelschwinghschule", "davertschule", "dietrich-bonhoeffer-schule", "dreifaltigkeitsschule", "eichendorffschule-angelmodde", "gottfried-von-cappenberg-schule", "hermannschule", "idaschule", "idaschule2","johannisschule", "kardinal-von-galen-schule", "kinderhaus-west", "kreuzschule", "loevelingloh", "ludgerusschule-albachten", "ludgerusschule-hiltrup","margaretenschule", "marienschule-hiltrup", "martin-luther-schule","martinischule", "matthias-claudius-schule","mauritzschule","melanchthonschule","michaelschule","mosaik-schule","norbertschule","overbergschule", "paul-gerhardt-schule", "paul-schneider-schule", "peter-wust-schule","pleisterschule","poetterhoekschule","primus-schule","grundschule-sprakel","theresienschule","thomas-morus-schule","wartburg-grundschule","adolph-kolping-berufskolleg","adolph-kolping-berufskolleg-2","adolph-kolping-berufskolleg-3","anne-frank-berufskolleg","annette-von-droste-huelshoff-gymnasium","augustin-wibbelt-schule","erna-de-vries-realschule","freiherr-vom-stein-gymnasium","friedensreich-hundertwasser-schule","geistschule","gesamtschule-muenster-mitte" , "geschwister-scholl-gymnasium", "paulinum","gymnasium-wolbeck","hansa-berufskolleg","hans-boeckler-berufskolleg","hauptschule-coerde","johann-conrad-schlaun-gymnasium","ludwig-erhard-berufskolleg","mathilde-anneke-gesamtschule","pascal-gymnasium","ratsgymnasium","realschule-im-kreuzviertel","beckstrasse","richard-von-weizsaecker-schule","schillergymnasium","uppenbergschule","waldschule-kinderhaus","wilhelm-emmanuel-von-ketteler-berufskolleg","wilhelm-hittorf-gymnasium","kita-albachten","kita-am-edelbach","kita-inselbogen","kita-wolbeck","kita-berg-fidel","kita-brueningheide","kita-burgwall","kita-handorf","kinderhaus-west-1","kita-emmerbachtal","kita-gievenbeck","kita-in-der-alten-schule","kita-kinderhaus","kita-legdenweg","kita-loddengrund","kita-mecklenbeck","kita-normannenweg","kita-drostenhof","kita-am-gievenbach","kita-hiltrup-west","kita-im-moorhock","kita-killingstrasse","kita-rumphorst","kita-sonnentau","kita-wielerort","kita-wilkinghege","dreifachsportanlage","grosssporthalle-berg-fidel","sportanlage-hiltrup-sued","sportanlage-sentruper-hoehe","sporthalle-mosaik-schule","sporthalle-ost"]
#immobilien = ["stadthaus-2"]
service = Service('/Users/Real/chromedriver')
url_base = 'https://www.stadt-muenster.de/immobilien/umwelt-und-energie/lastganganalyse/smartoptimo-standorte/'
urls = [url_base + i for i in immobilien]

#hierarchy: id > name > class
def get_plain_text(url, energie):
    driver = webdriver.Chrome(service=service)
    #Vorbereitungen: Pointer im quellcode ausfindig machen

    if energie == 'Wärme':
        value1 = "//a[@title='Wärmezähler auswählen']"
        value2 = "//a[@title='Wasserverbrauch als Tabelle darstellen']"
    elif energie == 'Strom':
        value1 = "//a[@title='Stromzähler auswählen']"
        value2 = "//a[@title='Stromverbrauch als Tabelle darstellen']"
    elif energie == 'Wasser':
        value1 = "//a[@title='Wasserzähler auswählen']"
        value2 = "//a[@title='Wasserverbrauch als Tabelle darstellen']"

    #get to main page
    driver.get(url)

    #get to frame quellcode
    frames = driver.find_element(by=By.TAG_NAME, value= "iFrame")
    src = frames.get_attribute("src")
    driver.get(src)

    #get desired dataset (Strom, Wärme, Wasser) + Tag
    try:
        energy = driver.find_element(by=By.XPATH, value= value1)
        href = energy.get_attribute('href')
        driver.get(href)
    except:
        #print(energie + '-daten sind nicht vorhanden')
        thewriter.writerow({'Immobilie': immobilien[counter], 'Datum': 'x', 'Energietyp': energie, 'Verbrauch' : 'No Data'})
        return

    # get Tabelle
    element = driver.find_element(by=By.XPATH, value=value2)
    hrefbase = element.get_attribute('href')
    for date in adjDateList[1:]:  #iterieren durch tage
        href = hrefbase.replace('t' + str(b), 't' + date) #gewünschten Tag auswählen
        driver.get(href)  
        print(href)

        #speichere quellcode
        plain_text = driver.page_source
        main_spider(plain_text, energie)
    driver.quit()


def main_spider(plain_text, energie):
    soup = BeautifulSoup(plain_text, "lxml")
    Datum = []
    for entry in soup.findAll('td', class_='first'):
            Datum.append(entry.text)

    Verbrauch = []
    for entry in soup.findAll('td', align='right'):
        if entry.text != ' ':       #!!!: wenn eine Zeile empty (durch Fehler etc.) dann verschiebt sich Datensatz
            Verbrauch.append(entry.text)

    x = zip(Datum, Verbrauch)
    for i, j in x:
        if i != 'Summe' and j != ' ':
            thewriter.writerow({'Immobilie': immobilien[counter], 'Datum': i, 'Energietyp': energie, 'Verbrauch': j})

#Initialize Function
Energietyp = ['Wärme', 'Strom', 'Wasser']
with open('Energiedaten.csv', 'w', newline='') as f:
    thewriter = csv.DictWriter(f, fieldnames=Header)
    thewriter.writeheader()
    counter = 0
    for url in urls:
        for energie in Energietyp:
            get_plain_text(url,energie)
        counter += 1