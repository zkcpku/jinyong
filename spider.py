#CrowTaobaoPrice.py
import requests
import re

txtName = '鸳鸯刀'
start_url = 'http://www.jinyongwang.com/yuan/'
start_chapter = '鸳鸯刀'
end_chapter = '鸳鸯刀'
need_sort = False
need_reverse = False

def getHTMLText(url):
	try:
		headers = {'content-type': 'application/json',
		'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.4.4; en-US; XT1022 Build/KXC21.5-40) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.7.0.636 U3/0.8.0 Mobile Safari/534.30'}
		r = requests.get(url, timeout=30,headers = headers)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return ""

def txtInit():
	with open("txt/"+ txtName + ".txt","w",encoding = 'utf-8') as txtFile:
		txtFile.write('\n' + txtName + '\n\n')

def txtWrite(stmp):
	with open("txt/"+ txtName + ".txt","a",encoding = 'utf-8') as txtFile:
		txtFile.write(stmp + '\n')

def getContent(url):
	beginning = False
	html = getHTMLText(url)
	ContentList = []
	if html:
		plt = re.findall(r'<a href=".+?">.+?</a>',html)
		for s in plt:
			ss = re.split(r'["<>]',s)
			if len(ss) > 4 and ss[4] == start_chapter:
				beginning = True

			if beginning:
				ContentList.append([ss[2],ss[4]])

			if len(ss) > 4 and ss[4] == end_chapter:
				beginning = False
	return ContentList



def getChapter(url):
	chapterContent = getHTMLText(url)
	plt = re.findall(r'<p>.+?</p>',chapterContent)
	for e in plt:
		txtWrite(e[3:-4])
	return plt
 

def main():
	txtInit()
	# startNum = 17
	pre_url = 'http://www.jinyongwang.com'
	ContentList = getContent(start_url)


	if need_sort:
		lenC = len(ContentList)
		for i in range(0,lenC):
			for j in range(i + 1,lenC):
				if ContentList[i][1] > ContentList[j][1]:
					ctmp = ContentList[i]
					ContentList[i] = ContentList[j]
					ContentList[j] = ctmp

	if need_reverse:
		print(ContentList)
		r_ContentList = []
		lenC = len(ContentList)
		for i in range(0,lenC):
			j = lenC - i - 1
			r_ContentList.append(ContentList[j])
		ContentList = r_ContentList
		print(ContentList)

	for e in ContentList:
		now_url = pre_url + e[0]
		print(now_url,e[1])
		txtWrite('\n')
		txtWrite(e[1])
		txtWrite('\n')
		content = getChapter(now_url)
	 
if __name__ == '__main__':
	main()
