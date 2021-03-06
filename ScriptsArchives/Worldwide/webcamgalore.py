"""
--------------------------------------------------------------------------------
Descriptive Name     : webcamgalore.py
Author               : Ali Cataltepe						      
Contact Info         : ali@cataltepe.com
Date Written         : July 13, 2016
Description          : Parses the hourly snapshots from the aggregator website webcamgalore.com, putting US and non-US cameras into separate output files.
Command to run script: python webcamgalore.py
Usage                : N/A
Input file format    : N/A
Output               : list_webcamgalore.txt, list_US_webcamgalore.txt
Note                 : Should be only a substitute until we can find a way to parse most of the Flash video feeds the website links to.
Other files required by : Geocoding.py (NetworkCameras/Discovery/Tools/Geocoding.py)
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : webcamgalore.com
In database (Y/N)    : Y
Date added to Database : July 25, 2016
--------------------------------------------------------------------------------
"""

geocodingKeys=['''Put geocoding keys here''']
stopwords = ['what','who','is','a','at','is','he','towards','toward','webcam','view','over']

from selenium import webdriver
import urllib
from Geocoding import Geocoding
import time
from string import ascii_lowercase

# get_text_excluding_children() provided by 'Louis' on Stack Overflow (http://stackoverflow.com/a/19040341)
def get_text_excluding_children(driver, element):
	return driver.execute_script("""
	var parent = arguments[0];
	var child = parent.firstChild;
	var ret = "";
	while(child) {
    	if (child.nodeType === Node.TEXT_NODE)
        	ret += child.textContent;
    	child = child.nextSibling;
	}
	return ret;
	""", element)

def webcamgaloreNavigate():
	cameraPageLinks = []
	driver = webdriver.Firefox()
	geocoder = Geocoding("Google",geocodingKeys[0])
	API_num = 0
	for i in ascii_lowercase:
		masterList="https://www.webcamgalore.com/EN/complete-"+i+".html"
		driver.get(masterList);
		time.sleep(1)
		for elem in driver.find_elements_by_xpath("/html/body/table/tbody/tr/td[@valign='top']/a"):
			print elem.get_attribute("href")
			cameraPageLinks.append(elem.get_attribute("href"))
	USLinks = [link for link in cameraPageLinks if "USA" in link]
	for i in USLinks:
		cameraPageLinks.remove(i)
	listfile = open("list_webcamgalore.txt", "a")
	listfile.write("country#city#snapshot_url#latitude#longitude\n")
	time.sleep(0.5)
	for i in cameraPageLinks:
		driver.get(i)
		try:
			locationString = get_text_excluding_children(driver, driver.find_element_by_xpath("/html/body/table/tbody/tr/td[@valign='top']/h1"))
			if "Several" not in locationString:
				country = locationString.split(":")[0].split(",")[-1].strip()
				city = locationString.split(":")[0].split(",")[0].strip()
				locat = locationString.split(":")[1].strip()
				locatwords = locat.split()
				resultwords  = [word for word in locatwords if word.lower() not in stopwords]
				locat = ' '.join(resultwords)
				state = ""
				print locat
				locat = locat.encode('utf-8').replace("ë","e").replace("ö","o").replace("ß","s").replace("Ö","O").replace("Ë","E").replace("ẞ","S").replace("ş","s").replace("Ş","S").replace("Ç","C").replace("ç","c").replace("ı","i").replace("İ","I").replace("â","a").replace("é","e").replace("Î","I").replace("î","i").replace("É","E").replace("è","e").replace("È","E").replace("À","A").replace("à","a").replace("ü","u").replace("Ü","U").replace("ğ","g").decode('utf-8')
				state = state.encode('utf-8').replace("ë","e").replace("ö","o").replace("ß","s").replace("Ö","O").replace("Ë","E").replace("ẞ","S").replace("ş","s").replace("Ş","S").replace("Ç","C").replace("ç","c").replace("ı","i").replace("İ","I").replace("â","a").replace("é","e").replace("Î","I").replace("î","i").replace("É","E").replace("è","e").replace("È","E").replace("À","A").replace("à","a").replace("ü","u").replace("Ü","U").replace("ğ","g").decode('utf-8')
				city = city.encode('utf-8').replace("ë","e").replace("ö","o").replace("ß","s").replace("Ö","O").replace("Ë","E").replace("ẞ","S").replace("ş","s").replace("Ş","S").replace("Ç","C").replace("ç","c").replace("ı","i").replace("İ","I").replace("â","a").replace("é","e").replace("Î","I").replace("î","i").replace("É","E").replace("è","e").replace("È","E").replace("À","A").replace("à","a").replace("ü","u").replace("Ü","U").replace("ğ","g").decode('utf-8')
				country = country.encode('utf-8').replace("ë","e").replace("ö","o").replace("ß","s").replace("Ö","O").replace("Ë","E").replace("ẞ","S").replace("ş","s").replace("Ş","S").replace("Ç","C").replace("ç","c").replace("ı","i").replace("İ","I").replace("â","a").replace("é","e").replace("Î","I").replace("î","i").replace("É","E").replace("è","e").replace("È","E").replace("À","A").replace("à","a").replace("ü","u").replace("Ü","U").replace("ğ","g").decode('utf-8')
				if len(locationString.split(":")[0].split(",")) > 2:
					locat+=(" "+locationString.split(":")[0].split(",")[1])
				try:
					snapshot_link = urllib.quote(driver.find_element_by_xpath("/html/body/table/tbody/tr/td[@valign='top']/table[2]/tbody/tr/td[@style='padding-left:10px']/center/a/img").get_attribute("src"), safe = ':?,=/&')
				except:
					try:
						snapshot_link = urllib.quote(driver.find_element_by_class_name("webcam-image").get_attribute("src"), safe = ':?,=/&')
					except:
						pass
				try:
					geocoder.locateCoords(locat, city, state, country)
					geocoder.reverse(geocoder.latitude, geocoder.longitude)
					info = geocoder.country + '#' + state + '#' + geocoder.city + '#' + snapshot_link + '#' + str(geocoder.latitude) + '#' + str(geocoder.longitude)
					print info
					listfile.write(info.replace(" ","").replace("##", "#").replace("\n",'')+'\n')
				# API key cycling courtesy of Ryan
				except Exception as error:
					if str(error) == "Your request was denied." or str(error) == "The given key has gone over the requests limit in the 24 hour period or has submitted too many requests in too short a period of time.":
						API_num = API_num+1
						if API_num < len(geocodingKeys):
							geocoder = Geocoding("Google", geocodingKeys[API_num])
						else:
							print "<<<ERROR:"+str(error)+">>>"
							print "API list exhausted, stopped on:"
							print geocoder.country+"#"+snapshot_link+"#"+str(geocoder.latitude)+"#"+str(geocoder.longitude)+"#"+"ERROR"+"#"+"ERROR"
							return
					else:
						print "<<<Error:"+str(error)+">>>"+" For:\n"+geocoder.country+"#"+snapshot_link+"#"+str(geocoder.latitude)+"#"+str(geocoder.longitude)+"#"+"ERROR"+"#"+"ERROR"
						pass
		except:
			pass
	listfileUS = open("list_US_webcamgalore.txt", "a")
	listfileUS.write("country#state#city#snapshot_url#latitude#longitude\n")
	time.sleep(0.5)
	for i in USLinks:
		driver.get(i)
		try:
			locationString = get_text_excluding_children(driver, driver.find_element_by_xpath("/html/body/table/tbody/tr/td[@valign='top']/h1"))
			if "Several" not in locationString:
				country = locationString.split(":")[0].split(",")[-1].strip()
				city = locationString.split(":")[0].split(",")[0].strip()
				locat = locationString.split(":")[1].strip()
				locatwords = locat.split()
				resultwords  = [word for word in locatwords if word.lower() not in stopwords]
				locat = ' '.join(resultwords)
				state = locationString.split(":")[0].split(",")[1].strip()
				print locat
				locat = locat.encode('utf-8').replace("ë","e").replace("ö","o").replace("ß","s").replace("Ö","O").replace("Ë","E").replace("ẞ","S").replace("ş","s").replace("Ş","S").replace("Ç","C").replace("ç","c").replace("ı","i").replace("İ","I").replace("â","a").replace("é","e").replace("Î","I").replace("î","i").replace("É","E").replace("è","e").replace("È","E").replace("À","A").replace("à","a").replace("ü","u").replace("Ü","U").replace("ğ","g").decode('utf-8')
				state = state.encode('utf-8').replace("ë","e").replace("ö","o").replace("ß","s").replace("Ö","O").replace("Ë","E").replace("ẞ","S").replace("ş","s").replace("Ş","S").replace("Ç","C").replace("ç","c").replace("ı","i").replace("İ","I").replace("â","a").replace("é","e").replace("Î","I").replace("î","i").replace("É","E").replace("è","e").replace("È","E").replace("À","A").replace("à","a").replace("ü","u").replace("Ü","U").replace("ğ","g").decode('utf-8')
				city = city.encode('utf-8').replace("ë","e").replace("ö","o").replace("ß","s").replace("Ö","O").replace("Ë","E").replace("ẞ","S").replace("ş","s").replace("Ş","S").replace("Ç","C").replace("ç","c").replace("ı","i").replace("İ","I").replace("â","a").replace("é","e").replace("Î","I").replace("î","i").replace("É","E").replace("è","e").replace("È","E").replace("À","A").replace("à","a").replace("ü","u").replace("Ü","U").replace("ğ","g").decode('utf-8')
				country = country.encode('utf-8').replace("ë","e").replace("ö","o").replace("ß","s").replace("Ö","O").replace("Ë","E").replace("ẞ","S").replace("ş","s").replace("Ş","S").replace("Ç","C").replace("ç","c").replace("ı","i").replace("İ","I").replace("â","a").replace("é","e").replace("Î","I").replace("î","i").replace("É","E").replace("è","e").replace("È","E").replace("À","A").replace("à","a").replace("ü","u").replace("Ü","U").replace("ğ","g").decode('utf-8')
				try:
					snapshot_link = urllib.quote(driver.find_element_by_xpath("/html/body/table/tbody/tr/td[@valign='top']/table[2]/tbody/tr/td[@style='padding-left:10px']/center/a/img").get_attribute("src"), safe = ':?,=/&')
				except:
					try:
						snapshot_link = urllib.quote(driver.find_element_by_class_name("webcam-image").get_attribute("src"), safe = ':?,=/&')
					except:
						pass
				try:
					geocoder.locateCoords(locat, city, state, country)
					geocoder.reverse(geocoder.latitude, geocoder.longitude)
					info = geocoder.country + '#' + state + '#' + geocoder.city + '#' + snapshot_link + '#' + str(geocoder.latitude) + '#' + str(geocoder.longitude)
					print info
					listfileUS.write(info.replace(" ","").replace("##", "#").replace("\n",'')+'\n')
				# API key cycling courtesy of Ryan
				except Exception as error:
					if str(error) == "Your request was denied." or str(error) == "The given key has gone over the requests limit in the 24 hour period or has submitted too many requests in too short a period of time.":
						API_num = API_num+1
						if API_num < len(geocodingKeys):
							geocoder = Geocoding("Google", geocodingKeys[API_num])
						else:
							print "<<<ERROR:"+str(error)+">>>"
							print "API list exhausted, stopped on:"
							print geocoder.country+"#"+snapshot_link+"#"+str(geocoder.latitude)+"#"+str(geocoder.longitude)+"#"+"ERROR"+"#"+"ERROR"
							return
					else:
						print "<<<Error:"+str(error)+">>>"+" For:\n"+geocoder.country+"#"+snapshot_link+"#"+str(geocoder.latitude)+"#"+str(geocoder.longitude)+"#"+"ERROR"+"#"+"ERROR"
						pass
		except:
			pass
	driver.close()

if __name__ == '__main__':
	webcamgaloreNavigate()
