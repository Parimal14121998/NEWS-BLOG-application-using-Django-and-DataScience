from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .models import newsblogmodel
import requests
import bs4
import random
from django.core.mail import send_mail

#bots used for webscraping
user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]
# Create your views here.

def home(request):
	if request.user.is_authenticated:
		# ----- code to fetch and display news
		if(request.GET.get("btn")):
			try:
				a1="https://newsapi.org/v2/top-headlines"
				a2="?country=" + "in"
				a3="&apikey="+ "dcf42dec7d614e778d3dcd8616ab8182"
				wa=a1+a2+a3
				res=requests.get(wa)
				data=res.json()
				info=data["articles"]
				return render(request,"home.html",{"info": info})
			except Exception as e:
				return render(request,"home.html",{"info": e})
		if request.GET.get("close"):
			return render(request,"home.html")
		# ---- code to get gold and silver prices
		elif(request.GET.get("btngs")):
			rgold = requests.get('https://www.goodreturns.in/gold-rates/', headers={'User-Agent': random.choice(user_agents_list)})
			soup=bs4.BeautifulSoup(rgold.text,"html.parser")
			pricegold=soup.select("strong")[0].text

			rsilver = requests.get("https://www.goodreturns.in/silver-rates/#Today+24+Carat+Gold+Rate+Per+Gram+in+India+%28INR%29", headers={'User-Agent': random.choice(user_agents_list)})
			soup = bs4.BeautifulSoup(rsilver.text, 'html.parser')
			price = soup.find("div", class_="gold_silver_table right-align-content").find("tr", class_="odd_row").findAll("td")
			pricesilver = price[1].text
			msg1="Gold is "+ str(pricegold) +"/gm*" + "  & Silver is " + str(pricesilver) +"/gm*"
			return render(request,"home.html",{"gs": msg1})
		#---- code to get crypto prices
		elif(request.GET.get("btncr")):
			try:
				a1="http://api.coinlayer.com/live"
				a2="?access_key=" + "7cf1f40966f385c2b7121d4bd4ef71d8"
				wa=a1+a2
				res=requests.get(wa)
				data=res.json()

				rate1=data["rates"]['BTC']
				rate2=data["rates"]['ETH']
				rate3=data["rates"]['DOGE']
			
				msg2="Bitcoin = $"  + str(rate1) + "\nEthereum = $" + str(rate2) + "\nDogecoin = $" + str(rate3)
				return render(request,"home.html",{"cr":msg2})
			except Exception as e:
				return render(request,"home.html",{"issue :":e})
 
		else:
			return render(request,"home.html")

	else:
		return redirect("ulogin")

def ulogin(request):
	if request.user.is_authenticated:
		return redirect("home")
	elif request.method=="POST":
		un=request.POST.get("un")
		pw=request.POST.get("pw")
		usr=authenticate(username=un,password=pw)
		if usr is not None:
			login(request,usr)
			return redirect("home")
		else:	
			return render(request,"login.html",{"msg":"invalid username and password"})
	else:
		return render(request,"login.html")


def usignup(request):
	if request.user.is_authenticated:
		return redirect("home")
	elif request.method=="POST":
		un=request.POST.get("un")
		pw1=request.POST.get("pw1")
		pw2=request.POST.get("pw2")
		if pw1==pw2:
			try:
				usr=User.objects.get(username=un)
				return render(request,"signup.html",{"msg":"user already exists"})
			except User.DoesNotExist:
				usr=User.objects.create_user(username=un,password=pw1)
				usr.save()
				return redirect("ulogin")
		else:
			return render(request,"signup.html",{"msg":"passwords did not match"})
	else:
		return render(request,"signup.html")
			

def ulogout(request):
	logout(request)
	return redirect("ulogin")

# code for subscribing any blog topics and mail notification will be sent to user
def usubscribe(request):
	if request.method=="POST" and request.POST.get("b1"):
		em=request.POST.get("em")
		na=request.POST.get("na")
		G1=request.POST.get("g1")
		G2=request.POST.get("g2")
		G3=request.POST.get("g3")	
		G4=request.POST.get("g4")
		listgenre=[]
		if G1:
			listgenre.append(G1)
		if G2:
			listgenre.append(G2)
		if G3:
			listgenre.append(G3)
		if G4:
			listgenre.append(G4)
		print(listgenre)
		stringgenre=""
		stringgenre=','.join(listgenre)
		cost=len(listgenre)*50
		try:
			usrn=newsblogmodel.objects.get(email=em)
			return render(request,"sub.html",{"msg":"Already subscribed"})
		except newsblogmodel.DoesNotExist:
			if stringgenre != "":
				subject = "NEWSBLOG SUBSCRIPTION LETTER"
				text = "You have subscribed to blogs for Genre : " + stringgenre + " and your cost incurred : " + str(cost)
				from_email="DJMLtester@gmail.com"
				to_email=[str(em)]
				send_mail(subject,text,from_email,to_email)
				data=newsblogmodel(email=em,name=na,genre=stringgenre)
				data.save()
				return render(request,"sub.html",{"msg":"congrats for subscription"})
			else:
				return render(request,"sub.html",{"msg":"Please fill any one genre"})
	else:
		return render(request,"sub.html")



def uunsubscribe(request):
	if request.method=="POST":
		em=request.POST.get("em")
		try:
			usrn=newsblogmodel.objects.get(email=em)
			subject = "NEWSBLOG UNSUBSCRIPTION LETTER"
			text = "You have unsubscribed to blogs.Sorry to let u go .To resume check for offers"
			from_email="DJMLtester@gmail.com"
			to_email=[str(em)]
			send_mail(subject,text,from_email,to_email)
			usrn.delete()	
			return render(request,"unsub.html",{"msg":"sorry to let u go"})
		except newsblogmodel.DoesNotExist:
			return render(request,"unsub.html",{"msg":"email not subscribed in past"})
	else:
		return render(request,"unsub.html")