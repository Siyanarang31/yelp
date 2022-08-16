import scrapy
import re
import time
import configparser
from datetime import datetime
from time import sleep



config = configparser.RawConfigParser()
config.read(r'C:\Users\HP\yelp\yelp\spiders\config.ini')

country_code = config['PROPERTIES']['DOMAIN_COUNTRY_CODE']
 
# Creating a new class to implement Spide
class yelpSpider(scrapy.Spider):
 
    # Spider name
    name = config['PROPERTIES']['NAME']
 
    # Domain names to scrape
    allowed_domains = [f'yelp.{country_code}']

    start_urls=[]

    def __init__(self, myBaseUrl=None):
        #Number of Pages
        pages = config['PROPERTIES']['PAGES']
        #Base Url
        myBaseUrl = config['URL']['BASE_URL']
        print(myBaseUrl)

        # Creating list of urls to be scraped by appending page number at the end of base url
        for i in range(0,int(pages),10):
            print(self.start_urls.append(str(myBaseUrl)+str(i)))
    
    #  Defining a Scrapy parser
    def parse(self, response):
            start_date = config['DATE']['START']
            end_date = config['DATE']['END']

            minimum_comment_length = int(config['PROPERTIES']['MIN_COMMENT_LENGTH'])
            maximum_comment_length = int(config['PROPERTIES']['MAX_COMMENT_LENGTH'])  

            data = response.css('#main-content') 
             

 
        # Collecting product star ratings
            # star_rating = data.css(".i-stars__09f24__M1AR7::attr(aria-label)")
            # print(star_rating)

            # Collecting user names
            user_names = data.css(".css-1kb4wkh")
            

            #Collecting user urls
            user_urls = data.css('.css-1kb4wkh')

            # Collecting review titles
            # review_titles = data.css('.b w_Aw')
            # print(review_titles)

            # Collecting user reviews
            review_texts = data.css('.raw__09f24__T4Ezm')
            

            #Collecting review dates
            review_dates = data.css('.css-chan6m')

            # collecting review location
            review_loc= data.css ('.css-qgunke')
    

            #Collecting sub product names
 #           subproduct_namelinks = data.css('.review-data a')

            #Collecting votes
            #review_votes = data.css('.cr-vote-text')  '''


            count = 0
            item = dict()
            # Combining the results
            #for review in user_names:
            this_review_text = ''.join(review_texts[count].xpath(".//text()").extract())  #.replace("\n","").strip()
            this_review_date_string = ''.join(review_dates[count].xpath(".//text()").extract())  #.split(" on", 1)[1].strip()  

        
        # TRY AND EXCEPT IS DONE DUE TO THE DIFFERENT AMAZON DATE FORMATS OF REVIEWS
               # try:
                    #this_review_datetime = datetime.strptime(this_review_date_string, '%B %d %Y')
                #except:
            this_review_datetime = datetime.strptime(this_review_date_string, '%x')
            dateStart_datetime = datetime.strptime(start_date, '%x')
            dateEnd_datetime = datetime.strptime(end_date, '%x')

            if this_review_datetime >= dateStart_datetime and this_review_datetime <= dateEnd_datetime and len(this_review_text) > minimum_comment_length and len(this_review_text) < maximum_comment_length:
                    item.update({
                        'stars': "NA",
                        'username': ''.join(user_names[count].xpath(".//text()").extract()), #.replace("\n","").strip(),
                        'userurl': f'https://www.yelp.{country_code}' + ''.join(user_urls[count].xpath('//*[@id="main-content"]/div[2]/section[2]/div[2]/div/ul/li[1]/div/div[1]/div/div[1]/div/div/div[2]/div[1]/span/a').extract()),
                        'title': "NA",
                        'reviewtext': this_review_text,
                        'permalink': "NA",
                       'reviewlocation':review_loc, #re.search('Reviewed in(.+?)on', ''.join(review_dates[count].xpath(".//text()").extract())).group(1).strip(),
                        'reviewdate': this_review_date_string,
                        'subproductname': "NA",
                        'subproductlink':"NA",
                        'votes': "NA"
                    })
                    yield(item)
            count=count+1   