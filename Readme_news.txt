Title - NEWS app using django and datascience
WEBApp Link - http://pgnewsapp.pythonanywhere.com/ulogin

About - This project shows News to the authenticated users and subscription to blogs .

Overview:
The project is developed using django with model,view,templates architecture and extracting data from newsapi.org to gather and display news using datascience.
Alongside a Blog subscription concept is also used to subscribe/unsubscribe blogs and sending notifications over customer email using Django.

Django Concepts involved : MVT, CRUD , DTL , Authentication[USER object], Template Inheritance ,html render, redirect, django.core.mail 

DataScience : ETL is done using webscraping;API json response is used to parse relevant data and gain information from :-
1.https://newsapi.org/v2/top-headlines

Procedure:
1. views.py is written for code/logic .
2. templates is used for rendering html output
3. Template inheritance is used for similar layout using extends and block tag.
4. Data is fetched using api,json response,for which code is written in views.py
5. Two sqlite tables are included one for authentication and other for subscription users.
   User object is used for authentication management ie login/logout/signup and newsblogmodel(models.py) for blog subscription records.
6. Django CRUD operations are also used to save/ delete/create records for blog subscription users.
7. Email protocols are also used in settings.py to send mail notifications to customer to those who subscribe/unsubscribe specific blog content.








