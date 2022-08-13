# download-and-extract-zip-archive-files
This code uses a combination of selenium, beautifulsoup and the requests library to scrape, download, and extract zip archive files from a given url into a destination folder in your machine. 

## Why Selenium you ask!
Selenium has many browser automation capabilities. It is best to scrape data from websites which load intermittedly (loading DOM elements using JavaScript/Ajax). This means we need a way to wait for some DOM elements (ones you are interested in) because they may not be available before the website has fully loaded. Selenium WebDriverWait helps us do this.

## Browser driver
Make sure you have downloaded your browser drivers. If you are using Chrome, check the vsersion of your chrome browser, download chromedriver.exe https://chromedriver.chromium.org/downloads for the version, and saved it in your working directory. 
