import requests
import xml.etree.ElementTree as ET

tool = "xingyc0714@gmail.com"

# 设置数据库和搜索参数
db = "nucleotide"  # 指定数据库为核酸序列数据库
term = "Enterovirus D68[Organism] AND complete genome"  # 搜索术语，寻找 Enterovirus D68 的完整基因组
rettype = "xml"  # 返回结果类型为 XML
retmode = "xml"  # 返回模式为 XML

# 设置日期范围，从 2022 年 6 月 1 日到 2024 年 9 月 30 日
start_date = "2022-06-01"
end_date = "2024-09-30"
date_filter = f"sdate[{start_date}+TO+{end_date}]"  # 构建日期范围过滤器

# 构建搜索 URL
search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db={db}&term={term}&rettype={rettype}&retmode={retmode}&daterange={date_filter}&usehistory=y&tool={tool}"

# 发送请求到 NCBI 搜索接口
response = requests.get(search_url)

# 检查响应状态，如果成功，打印 XML 响应
if response.status_code == 200:
    print("Search successful, getting results...")
    xml_response = response.text
    
    # 使用 ElementTree 解析 XML 响应
    root = ET.fromstring(xml_response)
    
    # 初始化 WebEnv 和 QueryKey 变量
    web_env = None
    query_key = None
    
    # 遍历 XML 树，查找 WebEnv 和 QueryKey
    for child in root.iter():
        if child.tag == "WebEnv":
            web_env = child.text
        elif child.tag == "QueryKey":
            query_key = child.text
    
    # 检查是否成功获取 WebEnv 和 QueryKey
    if web_env and query_key:
        # 使用获取到的 WebEnv 和 QueryKey 构建 efetch URL 以检索详细信息
        fetch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={db}&WebEnv={web_env}&query_key={query_key}&rettype={rettype}&retmode={retmode}"
        
        # 发送请求到 efetch 接口
        fetch_response = requests.get(fetch_url)
        
        # 检查响应状态，如果成功，打印详细信息
        if fetch_response.status_code == 200:
            print("Fetch successful, here are the detailed results:")
            print(fetch_response.text)
        else:
            print("Failed to retrieve detailed data:", fetch_response.status_code)
    else:
        print("Failed to find WebEnv or QueryKey in the search response.")
else:
    print("Failed to search:", response.status_code)