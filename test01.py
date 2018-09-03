# coding=utf-8	

import urllib.parse
from urllib.request import urlopen 
from bs4 import BeautifulSoup 
import re
import datetime
import random 
import os
import shutil



saving_directory = "/Users/wanglixin/Documents/novel"
root_url = "http://www.8wenku.com"
pages = 50
page_url = "/book/"+str(pages)


def GetHtml(url):
	req = urllib.request.Request(url)
	req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)') 
	response = urllib.request.urlopen(req)  
	html = response.read()  
	return html  
	#return BeautifulSoup(html, "html.parser")


def GetObj(url, parser = "html.parser"):
	html = GetHtml(url)
	return BeautifulSoup(html, parser)


bsObj = GetObj(root_url+str(page_url))


# 首页检查



# 获取title，建立目录
title = bsObj.find("h2", {"class":"tit"}).get_text()
print("开始抓取"+title)
os.mkdir(saving_directory+"/"+title)

# 获取分卷链接，建立分卷目录
volume_list = []
chapter_list =[]

for vb in bsObj.find_all("a", href = re.compile("/volume/view")):
	volume_list.append(vb.get_text())
	print("抓取"+title+"_"+volume_list[-1])
	os.mkdir(saving_directory+"/"+title+"/"+volume_list[-1])
	volum_url = vb.get('href')
	S_Obj = GetObj(root_url+volum_url)

	#建立章节目录， 抓取内容
	for cb in S_Obj.find_all("a", href = re.compile("/chapter/view")):
		chapter_list.append(cb.get_text())
		print("抓取"+title+"_"+volume_list[-1]+"--"+chapter_list[-1])
		#os.mkdir(saving_directory+"/title/"+volume_list[-1]"/"+chapter_list[-1])
		chapter_url = cb.get('href')

		# 处理<br/> 插行

		# # html筛选处理
		# pre_html = GetHtml(root_url+chapter_url).replace(
		# 					bytes('<br />', encoding='utf8'),bytes('', encoding='utf8')).replace
		# Ss_Obj = BeautifulSoup(pre_html, "html.parser")
		# Ss_Obj.find("div", class_= "article-body").get_text()


		# get_text处理
		nm = GetObj(root_url+chapter_url)
		text = nm.find("div", class_= "article-body").get_text()
		text = text.replace('最新最全的日本动漫轻小说 轻小说文库(http://www.8wenku.com) 为你一网打尽！'
							,'').replace('\n','',2).replace(
							';9999999本文来自 轻小说文库(http://www.8wenku.com)','')
		OpStream = open(saving_directory+"/"+title+"/"+volume_list[-1]+"/"+chapter_list[-1]+".txt",'x')
		OpStream.write(text)
		OpStream.close()









	
	

