# coding=utf-8	

from bs4 import BeautifulSoup 
from urllib.request import urlopen 
import urllib.parse
import urllib.error
import re
import os
import shutil




saving_directory = "/Users/wanglixin/Documents/novel"
root_url = "http://www.8wenku.com"
pages = 801
page_limit = 900

print('-'*82)
print('-'*30+"海苔卷爬虫 version_1.0"+'-'*30)
print('-'*82)
print(
' ██░ ██  ▄▄▄       ██▓▄▄▄█████▓ ▄▄▄       ██▓ ▄▄▄██▀▀▀█    ██  ▄▄▄       ███▄    █ \n'+
'▓██░ ██▒▒████▄    ▓██▒▓  ██▒ ▓▒▒████▄    ▓██▒   ▒██   ██  ▓██▒▒████▄     ██ ▀█   █ \n'+
'▒██▀▀██░▒██  ▀█▄  ▒██▒▒ ▓██░ ▒░▒██  ▀█▄  ▒██▒   ░██  ▓██  ▒██░▒██  ▀█▄  ▓██  ▀█ ██▒\n'+
'░▓█ ░██ ░██▄▄▄▄██ ░██░░ ▓██▓ ░ ░██▄▄▄▄██ ░██░▓██▄██▓ ▓▓█  ░██░░██▄▄▄▄██ ▓██▒  ▐▌██▒\n'+
'░▓█▒░██▓ ▓█   ▓██▒░██░  ▒██▒ ░  ▓█   ▓██▒░██░ ▓███▒  ▒▒█████▓  ▓█   ▓██▒▒██░   ▓██░\n'+
' ▒ ░░▒░▒ ▒▒   ▓▒█░░▓    ▒ ░░    ▒▒   ▓▒█░░▓   ▒▓▒▒░  ░▒▓▒ ▒ ▒  ▒▒   ▓▒█░░ ▒░   ▒ ▒ \n'+
' ▒ ░▒░ ░  ▒   ▒▒ ░ ▒ ░    ░      ▒   ▒▒ ░ ▒ ░ ▒ ░▒░  ░░▒░ ░ ░   ▒   ▒▒ ░░ ░░   ░ ▒░\n'+
' ░  ░░ ░  ░   ▒    ▒ ░  ░        ░   ▒    ▒ ░ ░ ░ ░   ░░░ ░ ░   ░   ▒      ░   ░ ░ \n'+
' ░  ░  ░      ░  ░ ░                 ░  ░ ░   ░   ░     ░           ░  ░         ░ \n')
                                                                                   
print('target address: '+root_url)
print('start with page ', pages)	


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


def GetText(saving_directory, root_url, bsObj):
	# 获取title，建立目录
	title = bsObj.find("h2", {"class":"tit"}).get_text()
	print("开始抓取"+title)
	try:
		os.mkdir(os.path.join(saving_directory, title))
	except FileExistsError as e:
		print(e)
		print("删除原有目录")
		shutil.rmtree(os.path.join(saving_directory, title))
		os.mkdir(os.path.join(saving_directory, title))


	volume_list = ['']
	chapter_list =['']
	# volume
	for vb in bsObj.find_all("a", href = re.compile("/volume/view")):
		if volume_list.count(vb.get_text()) != 0:
			print("网页内存在重复卷目录："+title+"_"+vb.get_text())
			fixed_nm = vb.get_text().replace("/","·")+'0'+str(volume_list.count(vb.get_text()))
			print("重命名为"+title+"_"+fixed_nm)
			volume_list.append(vb.get_text())
		else:
			volume_list.append(vb.get_text())
			fixed_nm = vb.get_text().replace("/","·")

		print("抓取"+title+"_"+fixed_nm)
		os.mkdir(os.path.join(saving_directory, title, fixed_nm))
		volum_url = vb.get('href')
		S_Obj = GetObj(root_url+volum_url)

		# chapter
		for cb in S_Obj.find_all("a", href = re.compile("/chapter/view")):
			chapter_list.append(cb.get_text().replace("/","·"))
			print("抓取"+title+"_"+volume_list[-1]+"--"+chapter_list[-1])
			chapter_url = cb.get('href')

			# 处理<br/> 插行，使用get_text处理
			nm = GetObj(root_url+chapter_url)
			text = nm.find("div", class_= "article-body").get_text()
			text = text.replace('最新最全的日本动漫轻小说 轻小说文库(http://www.8wenku.com) 为你一网打尽！'
								,'').replace('\n','',2).replace(
								';9999999本文来自 轻小说文库(http://www.8wenku.com)','')
			# IO					
			with open(os.path.join(saving_directory, title, fixed_nm, 
						chapter_list[-1]+'.txt'), 'w') as OpStream:
				OpStream.write(text)
	print(title+"抓取完毕")
	print("-"*60)


while pages<=page_limit:	
	try:
		print("try to scrape page", pages)
		bsObj = GetObj(root_url+"/book/"+str(pages))
	except urllib.error.HTTPError as e:
		print(e)
		print("-"*60)
		pages += 1

	else:
		GetText(saving_directory, root_url, bsObj)
		pages += 1

print("\ntouch the limit, stop here")






		# try:
		# 	os.mkdir(saving_directory+"/"+title+"/"+volume_list[-1])
		# except FileExistsError as e:
		# 	print("存在重复卷目录："+volume_list[-1])
		# 	print("重命名为")
		# else:
		# 	pass



			# OpStream = open(saving_directory+"/"+title+"/"+volume_list[-1]+
			# 				"/"+chapter_list[-1]+".txt",'w')
			# OpStream.close()





			# # html筛选处理
			# pre_html = GetHtml(root_url+chapter_url).replace(
			# 					bytes('<br />', encoding='utf8'),bytes('', encoding='utf8')).replace
			# Ss_Obj = BeautifulSoup(pre_html, "html.parser")
			# Ss_Obj.find("div", class_= "article-body").get_text()







