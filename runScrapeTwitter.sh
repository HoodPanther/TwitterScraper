cd /home/pi/TwitterScraper
echo "Running Twitter scraper at `date`" >> /tmp/pythonScraper.log
# python SearchAndStoreTweetsByKeywords.py
# python organizeFiles.py >> /tmp/pythonScraper.log
python update_db.py >> /tmp/pythonScraper.log
echo "python Twitter finished running at `date`" >> /tmp/pythonScraper.log
cd -
