
from utils import crawl_wiki, table_parser, table2img
import urllib.parse
import os 

pdf_outdir = 'output_pdfs'
img_outdir = 'output_imgs'

# start_url = 'https://zh.wikipedia.org/wiki/Main_Page'
# start_url = 'https://zh.wikipedia.org/wiki/Wikipedia:%E5%88%86%E9%A1%9E%E7%B4%A2%E5%BC%95'

# 获取所有页面的 URL
# all_urls = crawl_wiki.get_wikipedia_urls(start_url, max_url_num=1000)
with open("all_url.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# 移除每行末尾的换行符，并打印列表
all_urls = [line.strip() for line in lines]


# 打印所有获取到的 URL
for url in all_urls:

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
        json_str = df_filter.to_json(orient='records', force_ascii=False)

        # 将空值替换为空字符串
        df.fillna('', inplace=True)
    
        pdf_path = os.path.join(pdf_outdir,  decoded_entry.replace(':', '_') + '_' + str(tab_idx) + '.pdf')
        print(pdf_path)
        table2img.generate_table(df=df, pdf_path=pdf_path)

        noisy_image = table2img.pdf_to_images(pdf_path=pdf_path)

        if noisy_image is None:
            continue 
        noisy_image.save(os.path.join(img_outdir, decoded_entry.replace(':', '_') + '_' + str(tab_idx)+ '.png'), "PNG")
        

    
