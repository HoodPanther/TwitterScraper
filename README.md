# Twitter Scraper

A package to perform queries utilizing the Twitter API and save the results in an SQLite database file. The results are analyzed by counting the occurrence of specific words in the tweet message. The number of occurrencies are plotted as a function of time and the plots are published in a webpage served by Flask.

## Installation Instructions

Requirements:
sudo pip install flask-markdown
sudo apt-get install python-pandas
sudo pip install sqlalchemy
sudo pip install twython