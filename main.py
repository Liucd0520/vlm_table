
from utils import crawl_wiki, table_parser, table2img
import urllib.parse
import os 
import json 


pdf_outdir = 'output_pdfs'
img_outdir = 'output_imgs'
output_path = 'output.json'
url_path = 'all_url_10000.txt'

# start_url = 'https://zh.wikipedia.org/wiki/Main_Page'
# start_url = 'https://zh.wikipedia.org/wiki/Wikipedia:%E5%88%86%E9%A1%9E%E7%B4%A2%E5%BC%95'

# 获取所有页面的 URL
# all_urls = crawl_wiki.get_wikipedia_urls(start_url, max_url_num=1000)
with open(url_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

# 移除每行末尾的换行符，并打印列表
all_urls = [line.strip() for line in lines]



# 打印所有获取到的 URL
for url in all_urls:
    if 'Category' in url:
        continue

    # url = 'https://zh.wikipedia.org/wiki/Wikipedia:%E7%BB%9F%E8%AE%A1'
    
    print('url: ', url)
    decoded_entry = urllib.parse.unquote(url.split('/')[-1])
    try:
        tables = table_parser.parse_table(url)
    except:
        continue
    
    for tab_idx in range(len(tables)):

        df = tables[tab_idx]
        df_filter = table_parser.process_table(df)

        if df_filter is None:  # table 不能为空
            continue
        json_str = df_filter.to_dict(orient='records')

        # 将空值替换为空字符串
        df.fillna('', inplace=True)
        df = df.astype(str)  # 变成str类型，防止某些数据为int，而无法执行len(cell)操作

        pdf_path = os.path.join(pdf_outdir,  decoded_entry.replace(':', '_') + '_' + str(tab_idx) + '.pdf')
        try:
            table2img.generate_table(df=df, pdf_path=pdf_path)
        except:
            continue

        noisy_image = table2img.pdf_to_images(pdf_path=pdf_path)

        if noisy_image is None:
            continue 
        image_path = os.path.join(img_outdir, decoded_entry.replace(':', '_') + '_' + str(tab_idx)+ '.png')
        noisy_image.save(image_path, "PNG")

        result = {'url': url, 
                  'output': json_str, 
                  'image_path': image_path
                  }
        print(result)

        if os.path.exists(output_path):
            # 如果文件存在，读取现有数据
            with open(output_path, 'r', encoding='utf-8') as file:
                data_list = json.load(file)
        else:
            data_list = []

        data_list.append(result)
        with open(output_path, 'w',  encoding='utf-8') as file:
            json.dump(data_list, file, indent=4, ensure_ascii=False)

       
