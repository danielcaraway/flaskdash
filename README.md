To see dash dashboard, go to [url]/dash

```console
mkdir your_dashapp
cd your_dashapp
python3 -m venv venv
source venv/bin/activate
pip3 install flask
pip3 install gunicorn
pip3 install dash=1.8.0
pip3 freeze > requirements.txt
touch Procfile
touch .gitignore
```

### Add this to Procfile

```
web: gunicorn app:server 
```

### Add this to .gitignore

```
venv
history
*.pyc
.DS_Store
.env
```

### See it in action

```console
python app.py
```

### Push to heroku

```console
git init
heroku login
heroku create my_cool_dashapp
git add .
git commit -m "SO VERY DASHING"
git push heroku master
heroku open
```