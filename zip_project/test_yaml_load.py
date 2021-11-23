import yaml
import time

fpath = 'the_urge_todo.yaml'

with open(fpath,'r') as file:
	data = yaml.safe_load(file)
	#print(next(data))
	

print(data)

print(data['name'])

# print(data['name'])
# print(data['start_urls'])
# print(data['paginate_down_page'])
# print(data['paginate_horizontally'])
	
#print(next(data))

# while True:
# 	d = next(data)

# 	print(d)
# 	time.sleep(2)


{'name': 'The_Urge', 
'start_urls': ['https://theurge.com/'], 
'paginate_down_page': '(//*[@class="_3KP0F B3iaM"]/a)', 
'paginate_horizontally': '//*[@class="_3EoM2"]', 

'items': [
	{'price': None, 'xpath': '//*[@class="eP0wn _2xJnS"]', 
're': '\\d{1,3}(?:[.,]\\d{3})*(?:[.,]\\d{2})', 'string_replacements': [',', '']}, {'previous_price': None, 'xpath': '//*[@class="_2plVT"]'}, {'brand': None, 'xpath': '//*[@class = "URfXD"]/text()'}, {'description': None, 'xpath': '//*[@class = "_3I42k"]/text()'}, {'website': None, 'xpath': '//*[@class = "ZV4Wf"]/text()'}]}