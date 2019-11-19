# Warbler
![alt text](https://i.imgur.com/n3BB0gE.png)
Live demo available here: [warbwarb](https://warbwarb.herokuapp.com/) 
Please feel free to sign up a new account, or use the following test account. 
```
USERNAME: testuser 
PASSWORD: testuser
```

## Setup 
Create Python virtual enviorment: 
```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

Set up the database:
```
(venv) $ createdb warbler
(venv) $ python seed.py
```

Start the server:
```
(venv) $ flask run
```

In browser:
```
localhost:5000
```

## Intro

Warbler is a Twitter clone, the backend is built with Python and Flask. Users are able to sign up with a password protected account, edit profile, write posts, like posts, and follow users. Also included unit and integration tests. 

My partner and I specifically worked on:

* Homepage warbles
* User profile page details (location, bio, header image, total liked warbles)
* User cards that appear on followers, following and list-users pages
* Warble like/dislike button
* User profile edit authentication and update form
* Logout route
* Tests for user model, user views, message model, message views

