# -*- coding:utf-8 -*-

'''
获取百度贴吧数据
python 2.7.5
'''

import urllib2
import re


__author__ = 'hugo'


class FIX():
	# 去除img标签，7位长空格
	remove_img = re.compile('<img.*?>| {7}')
	# 去除超链接标签
	remove_addr = re.compile('<a.*?>|</a>')
	# 将换行符替换成\n
	replace_br = re.compile('<br><br><br><br>|<br><br><br>|<br><br>|<br>')

	def replace(self, x):
		x = re.sub(self.remove_img, '', x)
		x = re.sub(self.remove_addr, '', x)
		x = re.sub(self.replace_br, '\n', x)

		return x.strip()


class BDTB():
	'''百度贴吧类，获取贴子信息'''

	# 初始化，传入基地址及是否只查看楼主发帖的参数
	def __init__(self, base_url, see_lz, page_num):
		self.base_url = base_url
		self.see_lz = '?see_lz' + str(see_lz)
		self.page_num = '&pn=' + str(page_num)
		self.fix = FIX()
		self.default_title = u'tieba_info'

	# 传入页码，获取该页帖子的代码
	def get_page(self, page=1):
		try:
			url = self.base_url + self.see_lz + self.page_num
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
		except urllib2.URLError as e:
			if hasattr(e, 'reason'):
				print u'连接百度贴吧失败，失败原因:' , e.reason
				return None

		else:
			return response.read().decode('utf-8')


	# 获取贴吧标题
	def get_title(self,page):
		# page = self.get_page(1)
		pattern = re.compile(r'.*?/><title>(.*?)</title>.*?', re.S)
		result = re.search(pattern,page)
		if result:
			return result.group(1).strip()
		else:
			return None
	
	# 提取帖子页数
	def get_page_num(self,page):
		# page = self.get_page(1)
		pattern = re.compile(r'.*?<span class="red">(.*?)</span>.*?', re.S)
		result = re.search(pattern, page)
		if result:
			return result.group(1).strip()
		else:
			return None


	# 设置写文件标题
	def set_file_title(self, title):
		if title==None:
			with open(self.default_title + '.txt','w+') as fp:
				self.file = fp
		else:
			with open(title + '.txt','w+') as fp:
				self.file = fp
		
	# 获取帖子内容
	def get_content(self):
		page = self.get_page(1)
		pattern = re.compile(r'.*?class="d_post_content j_d_post_content ">(.*?)</div>.*?', re.S)

		items = re.findall(pattern, page)
		floor = 1
		for item in items:
			print floor,u'楼-------------------------------------------------------------------------'
			print 'data:' + self.fix.replace(item)
			floor += 1


	def start(self):
		index_page = self.get_page(1)
		page_num = self.get_page_num(index_page)
		title = self.get_title(index_page)
		self.set_file_title(title)

		if page_num==None:
			print u'URL已经失效，请重试...'

		


if __name__ == '__main__':
	print 'hello!!'

	base_url = 'http://tieba.baidu.com/p/3138733512'

	tieba = BDTB(base_url, 1, 1)

	tieba.start()


	# print res
	# print tieba.get_title()
	# print tieba.get_page_num()
	# tieba.get_content()
