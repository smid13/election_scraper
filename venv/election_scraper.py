import requests
from bs4 import BeautifulSoup
import sys
import csv


url = str(sys.argv[1])
output_file = "data.csv"
r = requests.get(url)
html = r.text
soup = BeautifulSoup(html, "html.parser")
odkazy = soup.find_all("td",{"class" : "center"})
href_list = [(y.get("href")) for x in odkazy for y in x.find_all("a")]
for i in range(0,len(href_list)):
  href_list[i] = "https://volby.cz/pls/ps2017nss/" + href_list[i]
kody_obci = []
kody_obci_url = soup.find_all("td",{"class" : "cislo"})
for i in kody_obci_url:
  kody_obci.append(i.text)

seznam_url = []
nazev_obce = []
kod_obce = []
okrsek = []
a = 0
print("stahuji URL...")
for i in href_list:
  r= requests.get(i)
  html = r.text
  soup = BeautifulSoup(html, "html.parser")
  if soup.find("h2").text == "\nVýsledky hlasování za územní celky\n":
    seznam_url.append(i)
    h3_tags = soup.find_all("h3")
    nazev_obce.append(h3_tags[1].text.strip("\n").split(":")[1])
    kod_obce.append(kody_obci[a])
    okrsek.append("x")
    a += 1
  else:
    odkazy_okrsky = soup.find_all("td",{"class" : "cislo"})
    odkazy_okrsky_url = [(y.get("href")) for x in odkazy_okrsky for y in x.find_all("a")]
    for i in range(0,len(odkazy_okrsky_url)):
      odkazy_okrsky_url[i] = "https://volby.cz/pls/ps2017nss/" + odkazy_okrsky_url[i]
      h3_tags = soup.find_all("h3")
      nazev_obce.append(h3_tags[1].text.strip("\n").split(":")[1])
      kod_obce.append(kody_obci[a])
    [(okrsek.append(c.text)) for i in odkazy_okrsky for c in i.find_all("a")]
    a += 1
    seznam_url += odkazy_okrsky_url

volici_v_seznamu = []
vydane_obalky = []
platne_hlasy = []
platne_hlasy_strany = []
print("stahuji data....")
for i in seznam_url:
  r= requests.get(i)
  html = r.text
  soup = BeautifulSoup(html, "html.parser")
  volici_v_seznamu.append(soup.find("td",{"headers":"sa2"}).text)
  vydane_obalky.append(soup.find("td",{"headers":"sa3"}).text)
  platne_hlasy.append(soup.find("td",{"headers":"sa6"}).text)
  platne_hlasy_1 = soup.find_all("td",{"headers":"t1sb3"})
  platne_hlasy_2 = soup.find_all("td",{"headers":"t2sb3"})
  [(platne_hlasy_strany.append(hlasy.text)) for hlasy in platne_hlasy_1]
  [(platne_hlasy_strany.append(hlasy.text)) for hlasy in platne_hlasy_2]
url = seznam_url[0]
r = requests.get(url)
html = r.text
soup = BeautifulSoup(html, "html.parser")
seznam_stran_1 = soup.find_all("td",{"headers":"t1sb2"})
seznam_stran_2 = soup.find_all("td",{"headers":"t2sb2"})
seznam_stran = []
[(seznam_stran.append(strana.text)) for strana in seznam_stran_1]
[(seznam_stran.append(strana.text)) for strana in seznam_stran_2]

print("vytvařím csv")
header = ["Kód","Obec","Okrsek","Voliči v Seznamu","Vydané Obálky","PLatné Hlasy"]
[header.append(strana) for strana in seznam_stran]
data = []
[(data.append(list())) for i in range(0,len(seznam_url))]
for i in range(0,len(seznam_url)):
  data[i] = [kod_obce[i],nazev_obce[i],okrsek[i],volici_v_seznamu[i],vydane_obalky[i],platne_hlasy[i]]
a = 0
b = 30
for i in data:
  i.extend(platne_hlasy_strany[a:b])
  a += 30
  b += 30

with open(output_file, "w", encoding='UTF8', newline='') as f:
  writer = csv.writer(f)
  writer.writerow(header)
  writer.writerows(data)