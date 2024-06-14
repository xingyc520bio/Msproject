import requests

db = "nucleotide"
# 添加了 "complete genome" 术语
term = "Enterovirus D68[Organism] AND complete genome"
rettype = "xml"
retmode = "xml"
tool = "xingyc0714@gmail.com"  # 请替换为您的工具ID


# 设置日期范围
start_date = "2022-06-01"
end_date = "2024-09-30"
date_filter = f"sdate[{start_date}+TO+{end_date}]"

# 构建搜索 URL
search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db={db}&term={term}&rettype={rettype}&retmode={retmode}&daterange={date_filter}&usehistory=y&tool={tool}"

# 发送请求
response = requests.get(search_url)

# 检查响应状态
if response.status_code == 200:
    xml_response = response.text
    print(xml_response)
else:
    print("Failed to retrieve data:", response.status_code)