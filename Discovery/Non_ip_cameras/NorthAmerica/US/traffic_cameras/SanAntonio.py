
'''
This program will parse camera information from the San Antonio Department of Transportation website. It will utilize
selenium webdriver to deal with html source code generated by javascript. It will then implement Regex to extract
the relevant information and use Google API to convert street addresses to geo locations.
'''
from selenium import webdriver
import urllib2
import re
import json
import time

#This function initializes the webdriver to fetch the website
def getSANA():
    driver = webdriver.Firefox()
    driver.get("http://www.transguide.dot.state.tx.us/ITS_WEB/Frontend/default.html?r=SAT&p=San%20Antonio&t=cctv")
    time.sleep(5)
    file = open('SanAntonio_output.txt','w')
    getRoadway(driver,file)
    file.close()

#Due to the outline of the website where source url for cameras stored in tabs that represented by roadways, we can
#use selenium to emulate a click through each roadway
def getRoadway(driver,file):
    #Click through each roadway element
    driver.find_element_by_id('IH-10').click()
    driver.implicitly_wait(5)
    getCams(driver,file)
    driver.find_element_by_id('IH-35').click()
    driver.implicitly_wait(5)
    getCams(driver,file)
    driver.find_element_by_id('IH-37').click()
    driver.implicitly_wait(5)
    getCams(driver,file)
    driver.find_element_by_id('LP-1604').click()
    driver.implicitly_wait(5)
    getCams(driver,file)
    driver.find_element_by_id('LP-410').click()
    driver.implicitly_wait(5)
    getCams(driver,file)
    driver.find_element_by_id('SH 151').click()
    driver.implicitly_wait(5)
    getCams(driver,file)
    driver.find_element_by_id('US-281').click()
    driver.implicitly_wait(5)
    getCams(driver,file)
    driver.find_element_by_id('US-90').click()
    driver.implicitly_wait(5)
    getCams(driver,file)

#This function parses relevant information with Regex
def getCams(driver,file):
    html = driver.find_element_by_id('CameraList')
    elem = html.get_attribute('innerHTML')

    #parse image source url
    imglist=[]
    images = re.findall(r'src=".*?"', elem)
    for img in images:
        if '.JPG' in img:
            match = re.search('"(.*?)"', img)
            url = match.group(1)
            imglist.append(url)

    #Parse street address
    streetlist=[]
    latlist=[]
    lnglist=[]
    streets = re.findall(r'<div class="CameraIdElement">.*?</div>', elem)
    for ind in streets:
        match = re.search(r'<div class="CameraIdElement">(.*?)</div>', ind)
        line = match.group(1)
        if '&' in line:
            line = line.replace('&amp;','and')
        if "'" in line:
            line = line.replace("'","")
        streetlist.append(line)
        line1 = line.replace(" ","+")
        line2 = line1.strip()
        add = line2+'+'+'SanAntonio'
        api = 'http://maps.googleapis.com/maps/api/geocode/json?address='+add
        response = urllib2.urlopen(api).read()
        #Load by json module 
        parsed_json = json.loads(response)
        content = parsed_json['results']
        #Extract latitude and longitude from the API json code
        loc = content[0]
        geo = loc['geometry']
        location2 = geo['location']
        lat = location2['lat']
        lng = location2['lng']
        string_lat = str(lat)
        string_lng = str(lng)
        latlist.append(string_lat)
        lnglist.append(string_lng)
        time.sleep(0.1)

    #Write output to file
    iter=0
    while iter < len(imglist):
        output = streetlist[iter]+'#'+'San Antonio'+'#'+'TX'+'#'+'USA''#'+imglist[iter]+'#'+latlist[iter]+'#'+lnglist[iter]
        iter +=1
        print output
        file.write(output.encode('utf-8')+'\n')

if __name__ == "__main__":
    getSANA()

