# Using API for the Latest Genome 
### (from 2022.6-2024.6)
First, this is the code for searching the API of D68 Genome and VP1 using Python, I used Chinese annotation which is easy for me.

```python

import requests
from datetime import datetime, timedelta

# 设置搜索参数
db = "nucleotide"  # 搜索数据库
term = "Enterovirus D68[Organism]"  # 搜索术语
rettype = "xml"  # 返回数据格式
retmode = "xml"  # 返回模式
tool = "xingyc0714@gmail.com"  # 你的工具名称或邮箱，用于 API 记录

# 计算两年前的日期
two_years_ago = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
date_range = f"filter=sdate:{two_years_ago}-to-{datetime.now().strftime('%Y-%m-%d')}"

# 构造 E-utilities API URL
search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db={db}&term={term}&rettype={rettype}&retmode={retmode}&daterange={date_range}&usehistory=y&tool={tool}"

# 发送 HTTP GET 请求
response = requests.get(search_url)

# 检查响应状态
if response.status_code == 200:
    # 解析 XML 响应
    xml_response = response.text
    # 这里可以添加解析 XML 并提取需要的 ID 的代码
    print(xml_response)
else:
    print("Failed to retrieve data:", response.status_code)

# 请注意，这个脚本仅用于演示如何构造请求和获取响应。
# 实际的数据处理和序列检索需要进一步的逻辑来解析 XML 并使用 efetch.fcgi 获取序列数据。
 ```

Only script with no Annotation be like:
 ```python
import requests
from datetime import datetime, timedelta

db = "nucleotide"
term = "Enterovirus D68[Organism]"
rettype = "xml"
retmode = "xml"
tool = "xingyc0714@gmail.com"

two_years_ago = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
date_range = f"filter=sdate:{two_years_ago}-to-{datetime.now().strftime('%Y-%m-%d')}"

search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db={db}&term={term}&rettype={rettype}&retmode={retmode}&daterange={date_range}&usehistory=y&tool={tool}"

response = requests.get(search_url)

if response.status_code == 200:
    xml_response = response.text
    print(xml_response)
else:
    print("Failed to retrieve data:", response.status_code)

 ```
<br />I run it on the conda and get this one:

<img width="940" alt="image" src="https://github.com/xingyc520bio/Msproject/assets/49332831/2d52477d-e9d0-4bd6-b613-e946e90e1700">

<br />

## XML Result Analysis from NCBI E-utilities eSearch Service

The XML result provided is a response from the NCBI E-utilities' eSearch service, which includes the search for records related to Enterovirus D68 (EV-D68). Below is the analysis of the results:

### Search Result Count
- The search returned **5751 records**, indicating that there are a considerable number of entries related to Enterovirus D68.

### Return Result Settings
- `<RetMax>` is set to **20**, meaning this query can return up to 20 records at a time.
- `<RetStart>` is set to **0**, indicating that the returned records start from the first item.

### Query Key
- A `QueryKey` with a value of **1** is used to reference this specific set of search results in subsequent operations, such as eFetch.

### Web Environment
- A `WebEnv` identifier is provided, which may be used for session management on the NCBI website.

### List of Record IDs
- A list of **20 specific record IDs** are presented, which are the unique identifiers for the records returned in the search results.

### Translation Set
- The original search term "Enterovirus D68[Organism]" was translated to "*enterovirus D68*"[Organism], and the search was conducted within the "Organism" field.
- The `<TermSet>` tag shows the specific search term and field, `<Count>` shows the number of records found, and `<Explode>Y</Explode>` indicates that the search term was broken down into separate items for the search.

### Query Translation
- It shows the final search query, which is "*enterovirus D68*"[Organism], indicating that the search was conducted on the "Organism" field.

### Error and Warning List
- This XML result does not have `<ErrorList>` or `<WarningList>` tags, indicating that there were no issues or warnings with the search.

This result indicates that my search was successful. But I think 5751 result is beyond my expectation.

## Adjustment
-Based on the feedback, I used the field [SLEN] to adjust the query because the genome of the virus is approximately 7.3kb, so my query range is 7.0-7.5kb. This field allows me to select to limit the results to a specific sequence length. 

-I gave it a try, but conda gave me an error response. I suspect that the NCBI's esearch.fcgi interface does not support the direct use of [SLEN] as a filter key. In NCBI searches, the filter for sequence length should use the sizerange parameter. Additionally, the format of the filter needs to be adjusted to ensure it is correctly parsed.

<img width="504" alt="image" src="https://github.com/xingyc520bio/Msproject/assets/49332831/b0954a43-0562-4fc5-98da-625fdde0e6f2">



```python
import requests

db = "nucleotide"
term = "Enterovirus D68[Organism]"
rettype = "xml"
retmode = "xml"
tool = "xingyc0714@gmail.com"

# 设置序列长度范围为7000到7500个碱基对
min_length = 7000
max_length = 7500

# 构建序列长度过滤器
length_filter = f"sizerange:{min_length}+{max_length}"

# 设置日期范围
start_date = "2022-06-01"
end_date = "2024-09-30"
date_filter = f"sdate[{start_date}+TO+{end_date}]"

# 构建搜索 URL
search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db={db}&term={term}&rettype={rettype}&retmode={retmode}&daterange={date_filter}&filter={length_filter}&usehistory=y&tool={tool}"

# 发送请求
response = requests.get(search_url)

# 检查响应状态
if response.status_code == 200:
    xml_response = response.text
    print(xml_response)
else:
    print("Failed to retrieve data:", response.status_code)
```
```python
import requests

db = "nucleotide"
term = "Enterovirus D68[Organism]"
rettype = "xml"
retmode = "xml"
tool = "xingyc0714@gmail.com"

min_length = 7000
max_length = 7500

length_filter = f"sizerange:{min_length}+{max_length}"

start_date = "2022-06-01"
end_date = "2024-09-30"
date_filter = f"sdate[{start_date}+TO+{end_date}]"

search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db={db}&term={term}&rettype={rettype}&retmode={retmode}&daterange={date_filter}&filter={length_filter}&usehistory=y&tool={tool}"

response = requests.get(search_url)

if response.status_code == 200:
    xml_response = response.text
    print(xml_response)
else:
    print("Failed to retrieve data:", response.status_code)
```
Here is the result I obtained:
<img width="943" alt="image" src="https://github.com/xingyc520bio/Msproject/assets/49332831/20405269-40f9-4d90-9d9a-4ec6ea80acbb">

It's quite strange that I still got 5,751 matching items.

I tried the other way which is adding “complete genome”. The code is as followed:

```python
import requests

db = "nucleotide"
# 添加了 "complete genome" 术语
term = "Enterovirus D68[Organism] AND complete genome"
rettype = "xml"
retmode = "xml"
tool = "xingyc0714@gmail.com"  


# 设置日期范围
start_date = "2022-06-01"
end_date = "2024-09-30"
date_filter = f"sdate[{start_date}+TO+{end_date}]"

# 构建搜索 URL
search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db={db}&term={term}&rettype={rettype}&retmode={retmode}&daterange={date_filter}&filter={length_filter}&usehistory=y&tool={tool}"

# 发送请求
response = requests.get(search_url)

# 检查响应状态
if response.status_code == 200:
    xml_response = response.text
    print(xml_response)
else:
    print("Failed to retrieve data:", response.status_code)
```
This is what I get this time:

<img width="942" alt="image" src="https://github.com/xingyc520bio/Msproject/assets/49332831/65b57fc1-100f-409b-a9c9-1bec64ac3913">


It's quite peculiar that the result this time seems to be correct. The number 5751 in the search results is not the number of results returned by the current search, but rather the number of results retrieved in a previous search step. In the XML results, the actual number of search results is 735, which can be seen from the 735 tag.


The translation set shows 5751, which may be because the "Enterovirus D68[Organism]" term was expanded to include all related subitems in the search due to Explode=Y in the translation stack, resulting in a count of 5751. After I added the search condition "complete[All Fields] AND genome[All Fields]", the actual number of search results was reduced to 735. So there should be 735 genomic results, and I'm not sure if this is correct.

I really want to visually inspect the sequence information with my eye. I tried to export the code directly in the conda terminal using the following code.

```python
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
        if fetch_response.statu
        s_code == 200:
            print("Fetch successful, here are the detailed results:")
            print(fetch_response.text)
        else:
            print("Failed to retrieve detailed data:", fetch_response.status_code)
    else:
        print("Failed to find WebEnv or QueryKey in the search response.")
else:
    print("Failed to search:", response.status_code)
```
### Final Results

The ultimate outcome is the `result.txt` file, which displays parts of the sequences. For instance, sequences like Sequence 1 and Sequence 2 have very accurate lengths, being over 7,300 or 7,500 kilobases (kb), which should correspond to the genome. However, some are quite short, such as the third sequence, which only has a few hundred kilobases, leading to the suspicion that it might be just a part of a gene. Therefore, I am very uncertain whether this has been successful, and 735 results are still too many.

### Adjustment of the `term` Parameter

Here, we employ the previous `import.py` to inspect our search results.

#### 1. Change Method
First, we adopt the parameters suggested by Eero: `enterovirus D68[Organism] AND ((("full" OR "complete") AND "genome") OR 7000:7500[SLEN])`. The Python code is as follows:

```python
term = "enterovirus D68[Organism] AND (((\"full\" OR \"complete\") AND \"genome\") OR 7000:7500[SLEN])"
```
The results obtained are as follows: 
<img width="932" alt="image" src="https://github.com/xingyc520bio/Msproject/assets/49332831/ff7c1cbf-de85-4517-bc02-c7686f82f63e">
There are 2,461,407 results, which even include protein sequences. I believe the main reason is that the use of "OR" is not appropriate; it should be "AND". Otherwise, they will include all sequences with lengths between 7000 and 7500.

#### 2. Modify the Connector
We will change the connector from "OR" to "AND" in the above criteria, that is:
```python
term = "enterovirus D68[Organism] AND (((\"full\" OR \"complete\") AND \"genome\") AND 7000:7500[SLEN])"
```
The results obtained are as follows:
<img width="940" alt="image" src="https://github.com/xingyc520bio/Msproject/assets/49332831/05f5ed07-35dc-4348-a906-72c9ba687aea">
There are 734 results, only one less than what we obtained last time.

#### 3. Remove the [SLEN] condition. 
I considered whether removing the SLEN condition would yield the same results as those from Friday. Thus, I obtained the following code:

```python
term = "enterovirus D68[Organism] AND (((\"full\" OR \"complete\") AND \"genome\")"
```
Result obtained: 
<img width="936" alt="image" src="https://github.com/xingyc520bio/Msproject/assets/49332831/1e36a932-92b5-471e-afa0-71a6ce2cb3c9">
There are still 735 results, which are exactly the same as the results from Friday.

Therefore, we adjust the final code to be:
 ```python
import requests

db = "nucleotide"
term = "enterovirus D68[Organism] AND (((\"full\" OR \"complete\") AND \"genome\") AND 7000:7500[SLEN])"
rettype = "xml"
retmode = "xml"
tool = "xingyc0714@gmail.com"

min_length = 7000
max_length = 7500

length_filter = f"sizerange:{min_length}+{max_length}"

start_date = "2022-06-01"
end_date = "2024-09-30"
date_filter = f"sdate[{start_date}+TO+{end_date}]"

search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db={db}&term={term}&rettype={rettype}&retmode={retmode}&daterange={date_filter}&filter={length_filter}&usehistory=y&tool={tool}"

response = requests.get(search_url)

if response.status_code == 200:
    xml_response = response.text
    print(xml_response)
else:
    print("Failed to retrieve data:", response.status_code)
```
