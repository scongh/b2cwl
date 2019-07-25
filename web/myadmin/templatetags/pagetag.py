from django import template
register = template.Library()

# 自定义过滤器
# @register.filter
# def kong_upper(val):
#     return val.upper()

#  自定义标签
from django.utils.html import format_html
@register.simple_tag
# count总页数，p当前选中的页码，h表示一样有多少个页码
def showPage(count,request,h):
	# count = int(count)
	# 接受当前的页码数
	p = int(request.GET.get('page',1)) # 默认值为1
	start = p - int(h/2) # 开始页
	
	# 首页判断
	if(start<=0):
		start = 1 
	# 尾部判断
	elif(count<= p + int(h/2)):
		start = count-h + 1

	# 获取当前请求的所有参数
	data = request.GET.dict()
	args = ''
	for i,j in data.items():
		# print(i,j)
		if(i != 'page'):
			args += '&'+ i + '=' + j
	print(args)
	page_html = ''
	
	
	if(p>1):
		# 跳到首页
		page_html += '<li><a href="?page=1{}">«</a></li>'.format(args)
		# 下一页
		page_html += '<li><a href="?page={0}{1}">上一页</a></li>'.format((p-1),args)
	if(count<h):
		h = count
	for i in range(h):
		# print(start+i,end=' , ')
		# page_html += str(start+i)
		if(p == start+i):
			page_html += '<li class="am-active"><a href="?page={p}{args}">{p}</a></li>'.format(p=start+i,args=args)
		else:
			page_html += '<li><a href="?page={p}{args}">{p}</a></li>'.format(p=start+i,args=args)
	
	if(p<count):
		# 下一页		
		page_html += '<li><a href="?page={0}{1}">下一页</a></li>'.format((p+1),args)
		# 跳到尾页
		page_html += '<li><a href="?page={0}{1}">»</a></li>'.format(count,args)

	return format_html(page_html)