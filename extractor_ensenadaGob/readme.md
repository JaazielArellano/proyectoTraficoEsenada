import requests
import json 
from bs4 import BeautifulSoup


url="https://api.crossref.org/journals?query=AI+students"
response=requests.get(url)
json_response=response.json()
#print(json.dumps(json_response["message"]["items"],indent=4))

"""
lista_titulos=json_response["message"]["items"]
for titulo in lista_titulos:
     print("- ",titulo["title"])

"""     

for item in json_response["message"]["items"]:
     print ("-",item["title"])
     


"""
soup=BeautifulSoup(response.content,'html.parser')
print(soup.contents,"-------------"
      )

      
lista=["IA","AI","Artificial Intelligence"]
for variable in lista:
    url=("https://api.crossref.org/journals?query=%s"%(variable))
    response=requests.get(url)

#json_response=json.loads(response.content)
#print(json.dumps(json_response,ident=4))
    print(json.dumps(response.json()["message"]["total-results"]))
"""
#print(json.dumps(json_response,ident=4))
