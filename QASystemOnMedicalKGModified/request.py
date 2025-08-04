import urllib.request
from urllib import request, parse
import ssl
import requests
import re

# 用Get方式请求百度
response = urllib.request.urlopen('http://www.baidu.com')

# response 就是百度服务器返回的响应体，即网页源代码
print(response.read().decode('utf-8'))

# 使用ssl未经验证的上下文
context = ssl._create_unverified_context()

# 定义请求url和header
url = 'https: //biihu.cc//account/ajax/login_process/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0'
}

# 定义请求参数
dict = {
    'return_url': 'https://biihu.cc/',
    'user_name': 'xiaoshuaib@gmail.com',
    'password': '123456789',
    '_post_type':'ajax',
}

# 将请求的参数转化为byte
data = bytes(parse.urlencode(dict), 'utf-8')

# 封装request
req = request.Request(url, data=data, headers=headers, method='POST')

# 请求
response = request.urlopen(req, context = context)
print(response.read().decode('utf-8'))

# Get 请求
r = requests.get('https://api.github.com/events')
# 携带请求参数
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.get('https://httpbin.org/get', params=payload)
# 模拟浏览器访问
url = 'https://api.github.com/some/endpoint'
headers = {'user-agent': 'my-app/0.0.1'}
r = requests.get(url, headers=headers)
# 获取服务器文本响应内容
r = requests.get('https://api.github.com/events')
r.text
r.encoding
# 字节相应内容
r.content
# 获取响应码
r = requests.get('https://httpbin.org/get')
r.status_code
# 获取响应头
r.headers
# 获取Json响应内容
r = requests.get('https://api.github.com/events')
r.json()
# 获取socket流响应内容
r = requests.get('https://api.github.com/events', stream=True)
r.raw
r.raw.read(10)
# 设置超时
requests.get('https://github.com/', timeout=0.001)

# Post 请求
r = requests.post('https://httpbin.org/post', data = {'key':'value'})

# 在一个键里添加多个值
# 使用元组
payload_tuples = [('key1', 'value1'), ('key1', 'value2')]
r1 = requests.post('https://httpbin.org/post', data=payload_tuples)
# 使用字典
payload_dict = {'key1': ['value1', 'value2']}
r2 = requests.post('https://httpbin.org/post', data=payload_dict)
print(r1.text)
r1.text == r2.text
# True

# 请求时用json作为参数
url = 'https://api.github.com/some/endpoint'
payload = {'some': 'data'}
r = requests.post(url, json=payload)

# 上传文件
url = 'https://httpbin.org/post'
files = {'file': open('report.xls', 'rb')}
r = requests.post(url, files= files)
r.text

# 获取cookie信息
url = 'http://example.com/some/cookie/setting/url'
r = requests.get(url)
r.cookies['example_cookie_name']
# 'example_cookie_value'

# 发送cookie信息
url = 'https://httpbin.org/cookies'
cookies = dict(cookies_are='working')
r = requests.get(url, cookies=cookies)
r.text
# '{'"cookies": {"cookies_are": "working"}}'

# HTTP 请求
r = requests.put('https://httpbin.org/put', data = {'key':'value'})
r = requests.delete('https://httpbin.org/delete')
r = requests.head('https://httpbin.org/get')
r = requests.options('https://httpbin.org/get')

content = 'Xiaoshuaib has 100 bananas'
res = re.match('^Xi.*(d+)s.*s$', content)
'''
    ^ represents the beginning of the string;
    $ represents the ending of the string;
    Xi matches the part that begins with "Xi";
    . represents all single characters
    * matches the part before * 0 times or more.
    .* matches arbitrary characters 0 times or more.
    d represents arbitrary numbers.
    + matches arbitrary numbers 1 time or more.
    (d+) a capture group that matches 1 or more number characters.
    then stores the matching number string.
    s represents all space characters.
    s$ matches the string that ends with s.
'''
print(res.group(1))
res = re.match('^Xi.*?(d+)s.*s$')
print(res.group(1))

# If the string has an enter character.
content = """Xiaoshuaib has 100
bananas"""
res = re.match('^Xi.*?(d+)s.*s$', content, re.S)
print(res.group(1))

res = re.search('Xi.*?(d+)s.*s', content, re.S)
print(res.group(1))

content = """Xiaoshuaib has 100 bananas;
Xiaoshuaib has 100 bananas;
Xiaoshuaib has 100 bananas;
Xiaoshuaib has 100 bananas;"""

# 获取所有的100
res = re.findall('Xi.*?(d+)s.*?s;',content,re.S)
print(res)

# 替换
content = re.sub('d+','250',content)
print(content)

# 编译封装一下，便于以后复用
content = "Xiaoshuaib has 100 bananas"
pattern = re.compile('Xi.*?(d+)s.*s',re.S)
res = re.match(pattern, content)

print(res.group(1))