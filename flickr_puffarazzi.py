# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 09:09:07 2021

@author: adrianhughes
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
## run
## > python flickr_GetUrl.py tag number_of_images_to_attempt_to_download
from flickrapi import FlickrAPI
import pandas as pd
import csv
import requests
import os
import sys
import time

key='ed40ec13d2ab235b12763fb1ec2a4738'
secret='83dffa93059bb6fb'
tag='puffin'
MAX_COUNT = 500
def get_urls(image_tag,MAX_COUNT):
    flickr = FlickrAPI(key, secret)
    photos = flickr.walk(text=image_tag,
                            tag_mode='all',
                            tags=image_tag,
                            extras='url_o',
                            per_page=50,
                            sort='relevance')
    count=0
    urls=[]
    for photo in photos:
        if count< MAX_COUNT:
            count=count+1
            print("Fetching url for image number {}".format(count))
            try:
                url=photo.get('url_o')
                urls.append(url)
            except:
                print("Url for image number {} could not be fetched".format(count))
        else:
            print("Done fetching urls, fetched {} urls out of {}".format(len(urls),MAX_COUNT))
            break
    urls=pd.Series(urls)
    print("Writing out the urls in the current directory")
    urls.to_csv(image_tag+"_urls.csv")
    print("Done!!!")
    
def put_images(FILE_NAME):
    urls=[]
    with open(FILE_NAME,newline="") as csvfile:
            doc=csv.reader(csvfile,delimiter=",")
            for row in doc:
                if row[1].startswith("https"):
                    urls.append(row[1])
                    if not os.path.isdir(os.path.join(os.getcwd(),FILE_NAME.split("_")[0])):
                        os.mkdir(FILE_NAME.split("_")[0])
                        t0=time.time()
                        for url in enumerate(urls):
                            print("Starting download {} of ".format(url[0]+1),len(urls))
                            try:
                                resp=requests.get(url[1],stream=True)
                                path_to_write=os.path.join(os.getcwd(),FILE_NAME.split("_")[0],url[1].split("/")[-1])
                                outfile=open(path_to_write,'wb')
                                outfile.write(resp.content)
                                outfile.close()
                                print("Done downloading {} of {}".format(url[0]+1,len(urls)))
                            except:
                                    print("Failed to download url number {}".format(url[0]))
                                    t1=time.time()
                                    print("Done with download, job took {} seconds".format(t1-t0)) 
    
    
def main(): 
    #retrieve urls     
    get_urls(tag,MAX_COUNT)
    #download images
    put_images(tag + ".csv")
    
if __name__=='__main__':
    main()
    
