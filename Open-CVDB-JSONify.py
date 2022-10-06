# Open-CVDB-JSONify.py
# Script to grab current open cloud vulnderability database and create a single JSON file
# All credit to CloudVulnDB.org and github.com/wiz-sec/open-cvdb
# Author: Seth
# Created: 5-October-2022
# RequiredModules
import os #Inbuilt module used for directory listing
import yaml #Additional yaml module to understand input files
import json #Additional json module to output in json format
import datetime #Inbuilt load datetime module to set unique output filename
import requests #Inbuilt get content from web
from bs4 import BeautifulSoup # Additional Module to clean up web page for processing
import wget #inbuilt module to grab YAML files.
from os import listdir
#Variables
github_url = 'https://github.com/wiz-sec/open-cvdb/tree/main/vulnerabilities/'
path = '.\\' #use current path
date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") #get date and time into string for output file name
output_file = "OCVDB-"+date+".json" #set output file name with date
baseurl= 'https://raw.githubusercontent.com/wiz-sec/open-cvdb/main/vulnerabilities/'
page =requests.get(github_url) #Set variable for page to be opened and url to be concatenated 
# Text file of current Yaml Files on OCVDB
newfile = open('yamllinks.txt','w') # Creating a new file to store the yaml file links
# Clean Webpage for Processing
soup = BeautifulSoup(page.content) # make page readable
soup.prettify() # clean up the page
# Find all the links on the page that end in .yaml and write them into the text file
for anchor in soup.findAll('a', href=True): #look for links
    links = anchor['href']
    if links.endswith('.yaml'): #only use links that end in .yaml
        links= links.split('/')[-1]
        newfile.write(links + '\n') #write file name to list
        print (links + ' written to file') #belt and braces
newfile.close() #close file to ensure it saves
#Fetching the links for the Yaml file and downloading the files
with open('Yamllinks.txt', 'r') as links:
    for link in links:
        if link:
            yamllink = baseurl + (link.rstrip('\n'))
            print(yamllink + ' and the file ' + link + ' file download started')
            #response = requests.get(yamllink) #only gets page status
            response = wget.download(yamllink) #download file
            # with open(link.rstrip('\n'),'w') as output_zfile: #open file to write removing trailing /n 
            # output_zfile.write(response) #dump content into file
            print(" ")
            print(yamllink + ' file has downloaded\n') 
# Clean Up
print(newfile)
print(' being removed')
for newfile in listdir(path):
    if newfile.endswith('.txt'):
        os.remove(path + newfile)
print(newfile)
print(' has been removed')
#Processing files into json
with os.scandir(path) as dirlist: #get directory listing
    for entry in dirlist: #do the following for each entry in directory listing
        if entry.name.endswith(".yaml") and entry.is_file(): #but only do it for yaml files
            with open(entry.name, 'r', encoding='utf-8') as yaml_in, open(output_file, "a") as json_out: #force utf8 for yaml files being read and open output in append mode
                yaml_object = yaml.safe_load(yaml_in) # yaml_object will be a list or a dict
                json.dump(yaml_object, json_out, indent=4, sort_keys=False) #dump yaml data into a jsonfile and make it pretty
                json_out.write("\n")
                print(entry.name, "done") #on screen prompt for yaml file processed
print(" ")
print("Process complete, "+output_file+" created.") #all done 
print('Yaml files being removed')
for newfile in listdir(path):
    if newfile.endswith('.yaml'):
        os.remove(path + newfile)
print('Yaml files have been removed')