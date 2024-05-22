import requests
import re
import pandas as pd

headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

def parse_table(url):
    # url = 'https://zh.wikipedia.org/wiki/Wikipedia:%E7%BB%9F%E8%AE%A1'
    # url = 'https://zh.wikipedia.org/wiki/Help:%E7%9B%AE%E5%BD%95'
    
    # 发送请求获取 HTML 内容
    response = requests.get(url, headers=headers)
    
    # 使用 pandas.read_html 解析 HTML 内容并获取表格数据
    tables = pd.read_html(response.content)

    return tables


def process_table(table):
    
    del_list = ['机器人', '搜索引擎', '访问者来源', '编辑者来源', '全部空间']

    
    # 表格需要多于2行, 但是不能多于500行
    if len(table) < 2  or len(table) > 200:
        return

    col_names = table.columns.tolist()
    # 表格不能小于2列
    if len(col_names) < 2 or len(col_names) > 10:
        return
        
    # 表格如果没有真实含义的header 则删除
    if col_names[:2] == [0, 1]:
        return
    
    # 如果有多层Header（多层Header可能来源于合并表格），那么转换成新的header
    if isinstance(col_names[0], tuple):  # 如果多层，会以truple的形式
        # 让里面的'_' 变成'-' 以免与连接符_冲突
        col_names = [tuple(word.replace('_', '-') for word in tpl) for tpl in col_names]
        
        if len(col_names[0]) > 3 :
            return
            
        elif len(col_names[0]) == 2:  # 合并table的header
            col_names = ['_'.join(item) if item[0] != item[1] else item[0]  for item in col_names]
            table.columns = col_names
            
        elif len(col_names[0]) == 3:  # 对于三行的，直接组合
            col_names = ['_'.join(item) for item in col_names]
            table.columns = col_names
        
    # 如果列名的长度总和大于100，则删除
    if len(''.join(col_names)) > 100:
        return

    # 如果在删除字段表里则删除
    if any(re.search(keyword, ''.join(col_names)) for keyword in del_list):
        return
        
    
    return table
    
    

if __name__ == '__main__':

    url = 'https://zh.wikipedia.org/wiki/Wikipedia:%E7%BB%9F%E8%AE%A1'
    tables = parse_table(url)

    # 对获取某个页面上的所有表格执行如下筛选

    for table in tables:

        table = process_table(table)    
        if table is not None:  # 如果table 不为空
            print(table)
        

