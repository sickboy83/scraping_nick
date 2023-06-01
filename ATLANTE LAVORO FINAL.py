import json
import requests
from bs4 import BeautifulSoup

URL = "https://atlantelavoro.inapp.org/atlante_lavoro.php"
soup = BeautifulSoup(requests.get(URL).content, "html.parser")
out = {}

for item in soup.select('#accordion3 [role=tabpanel]:not(:has([role=tabpanel])) li'):
    tmp = [item.get_text(strip=True)]
    url2 = item.a['href']
    soup2 = BeautifulSoup(requests.get(URL[:32] + url2).content, "html.parser")
    while True:
        p = item.find_parent(role='tabpanel').find_previous_sibling(role='tab')
        if p:
            tmp = [p.get_text(strip=True), *tmp]
            item = p
        else:
            break
    d = out
    for i, v in enumerate(tmp):
        if i == len(tmp) - 2:
            d.setdefault(v, {})
            d = d[v]
        elif i == len(tmp) - 1:
            d[v] = {}
            titoli = {}
            #for e in soup2.select("div.row.iq-font-blue .col-sm-4"):
                #titoli.setdefault(e.get_text(strip=True), [])
            titoli["1 - ATTIVITÀ"] = [e.get_text(strip=True) for e in soup2.select('div[style*="background-color: #bbe8f84f"]')]
            titoli["2 - RISULTATI ATTESI"] = [e.get_text(strip=True) for e in soup2.select('p[style*="background-color: #f5e6a263"]')]
            titoli["3 - SCHEDA DI CASO"] = [(e.get_text(strip=True), e.a.get("href")) for e in soup2.select('div[style*="background-color: #ededed8c"]')]
            
            result = []
            cp2011 = soup2.find("div", attrs={"id": "cp2011"}).find_all("tr")
            for e in cp2011[1:]:
                result.append((e.find_all("td")[0].text, e.find_all("td")[1].text))
            titoli["4 - CP2011"] = result    
            ateco = soup2.find("div", attrs={"id": "ateco"}).find_all("tr")
            result = []
            for e in ateco[1:]:
                result.append((e.find_all("td")[0].text, e.find_all("td")[1].text))
            titoli["5 - ATECO"] = result 
            for x in titoli:
                d[v][x] = titoli[x]
        else:
            d.setdefault(v, {})
            d = d[v]
            
with open('atlante_lavoro.json', 'w') as f:
    json.dump(out, f)
with open('atlante_lavoro(utf8).json', 'w', encoding= "utf8") as f:
    json.dump(out, f, ensure_ascii=False)
