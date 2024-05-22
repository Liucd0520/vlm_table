url = 'https://zh.wikipedia.org/wiki/Wikipedia:%E6%96%B9%E9%87%9D%E8%88%87%E6%8C%87%E5%BC%95'
# url = 'https://zh.wikipedia.org/wiki/%E5%9C%8B%E6%97%97%E5%88%97%E8%A1%A8'

from utils import crawl_wiki, table_parser, table2img
import urllib.parse
import os 


decoded_entry = urllib.parse.unquote(url.split('/')[-1])
tables = table_parser.parse_table(url)

pdf_outdir = 'output_pdfs'
img_outdir = 'output_imgs'


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





