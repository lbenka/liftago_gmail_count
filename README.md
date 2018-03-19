## Liftago CLI for monthly spending

Script check your gmail account and shows you how much you spend on liftago this month.

It is mostly quickstart of google gmail script with simple query. 

# Start up 

- You need to allow read rights to your gmail -> Step 1 from [google qickstart](https://developers.google.com/gmail/api/quickstart/python)

- in your working directory create virtual environment `virtualenv --python=python3.6 venv`

- install needed libs `pip install -r requirements.txt`

- create alias in your `vim ~/.bashrc` and add `alias lift='~/random_projects/liftago/venv/bin/python ~/random_projects/liftago/liftago.py'`

# Example 
![example](docs/example.png)