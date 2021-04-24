from binance.client import Client
import json
import sys
from binance.enums import *
import time
from scrapping import scrap

with open('config.json') as json_file:
  config = json.load(json_file)

clientkey = config['client_key']
secretkey = config['secret_key']
devise = config["monnaie"]
temps = config["seconde"]
mise = config["mise_total"]
target0 = config["multiplicateur"]
id_client = config["token_client"]
id_channel = config["id_channel"]
client = Client(clientkey, secretkey)


def parser(array, file):
  with open(file, 'w+') as json_file:
    json.dump(array, json_file)


def decimal_str(x: float, decimals: int = 10) -> str:
  return format(x, f".{decimals}f").lstrip().rstrip('0')


def arrondir(targetfloat):
  oui = decimal_str(targetfloat)
  if targetfloat >=1 :
    targetf = round(targetfloat, 2)
    return str(targetf)
  else :
    c=0;f=0;go=True
    liste = list(oui)
    for nb in liste:
      if nb != '0' and nb != '.':
        go=False
        f+=1
      else:
        c+=1
    listef= []
    for i in range(c+3):
      listef.append(liste[i])
    targetf = ''.join(listef)
    return targetf


def valeur(token):
  u = client.get_historical_trades(symbol=str(token.upper() + devise))
  return float(u[499]['price'])


def can_afford():
	global devise
	balance_dispo = float(client.get_asset_balance(asset=devise)['free'])
	if mise > balance_dispo:  # verifie si les fonds sont suffisant
		print('dollar dispo :', client.get_asset_balance(asset=devise)['free'])
		print('pas assez de fond.')
		f = input('')
		sys.exit()


if client.ping() == {}:  # on ping le server
	print('connect to server..')
	if mise == "all":
		mise = float(client.get_asset_balance(asset=devise)['free'])
	can_afford()
	dispo1 = client.get_asset_balance(asset=devise)['free']
	print(devise, 'dispo :', dispo1)  # devise disponible sur le compte binance
	print('mise :', mise)
	print('Ready')
else:
  sys.exit()
stop = input('')
if stop == 'quit':
  sys.exit()
elif stop == 'auto':
	stop = scrap(id_channel, id_client)
name = str(stop.upper() + devise)

nbr = mise / valeur(stop)
print('achat possible de', nbr, stop.upper())
if nbr >= 1:  																			# si on peut acheter un nombre entier du coin
  nbr = int(nbr)  																	# on met le la quantité d'achat en type "int"
elif nbr < 1:  																			# si on ne peut peux pas acheter un nombre entier du coin
	c = 0  																						# on arrondie pour qu'il y ai le moins de caractere possible et on met la quantité d'achat en type "float"
	liste = []
	nbrs = str(nbr)
	for i in range(len(nbrs)):
		if nbrs[i] == "0" or nbrs[i] == ".":
			c += 1
			liste.append(nbrs[i])
		else:
			liste.append(nbrs[i])
			break
	x = ''.join(liste)
	nbr = float(x)


print('achat de', nbr, stop.upper(), "/", devise, "...")
ordre1 = client.create_order(
	symbol=name,
	side=SIDE_BUY,
	type=ORDER_TYPE_MARKET,
	quantity=nbr)
print('check achat\n---------------')

prix_achat = float(ordre1['fills'][0]['price'])
#prix_achat = 10.02240000
print('prix achat :', prix_achat)
target = prix_achat*target0

arr = arrondir(target)
ordre_limit = client.order_limit_sell(symbol=name, quantity=nbr, price=arr)
print('limit vente :', arr)


order_id = ordre1['orderId']
#order_id = 399016912
#print('id ordre :', order_id)

valeur_achat = prix_achat*nbr


print('---------------\nvente dans', temps,'secondes\n---------------')

t0=round(time.time(), 4)
tf=t0+temps
on=True; vente=False
while on==True:
	#affichage du multiplicateur benef (ca sert a rien mais c jolie :p)
	benefice = valeur(stop)/valeur_achat
	print('x', benefice)
	if round(time.time(), 4) >= tf:
		on=False
		print("---------------")
		if ordre_limit['status'] == 'NEW':
			result = client.cancel_order(symbol=name, orderId=ordre_limit['orderId'])
			print('vente de', nbr, stop.upper(), "/", devise, "...")
			order = client.create_order(symbol=name,side=SIDE_SELL,type=ORDER_TYPE_MARKET,quantity=nbr)
		else:
			print('target atteinte !')



"""print('vente de', nbr, stop.upper(), "/", devise, "...")
order = client.create_order(
	symbol=name,
	side=SIDE_SELL,
	type=ORDER_TYPE_MARKET,
	quantity=nbr)
print('check vente')"""


time.sleep(2)
print(devise, 'dispo :', client.get_asset_balance(asset=devise)['free'])  # dollars dispo
dispo2 = client.get_asset_balance(asset=devise)['free']
print('benef sur le pump : x',float(dispo2)/float(dispo1))
fin = input('')