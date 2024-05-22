
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import pandas as pd
import random
from PIL import Image, ImageOps, ImageFilter
import numpy as np
from pdf2image import convert_from_path
from PIL import Image, ImageFilter
import random
import fonts
from reportlab.lib.styles import  ParagraphStyle


def generate_table(df, pdf_path):

    # 设置中文字体文件路径
    simsum_font_path = 'fonts/SimSun.ttf'
    simhei_font_path = 'fonts/SimHei.ttf'

    # 注册中文字体
    pdfmetrics.registerFont(TTFont('SunFont', simsum_font_path))
    pdfmetrics.registerFont(TTFont('SimHei', simhei_font_path))

    addMapping('SunFont', 0, 0, 'SunFont')  # 将字体映射为编码0
    addMapping('SimHei', 1, 1, 'SimHei')  # 将字体映射为编码0

    # 创建 PDF 文档
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)

    col_names = df.columns.values.tolist()
    print('xxx', col_names)

    # 针对header的差异，如果是多级就转置，但级就保持不变
    if  isinstance(col_names[0], tuple):
        col_names =  [[row[i] for row in col_names] for i in range(len(col_names[0]))]    
    else:
        col_names = [col_names]  # shape: [1, col]
    
    # print(len(col_names))
    len_title = len(col_names)
    header_column_nums = len(col_names[0])

    data = col_names + df.values.tolist()

    print(data)
    print(len(data[0]), len(data))
    # # 创建样式
    # styles = getSampleStyleSheet()
    # styleN = styles['Normal']

    # 自定义一个段落样式来处理表格中的文本，也就是处理行长文本的问题
    table_paragraph_style = ParagraphStyle(
        'table_paragraph',
        # parent=styles['Normal'],
        fontName='SunFont',
        # wordWrap='CJK',
        # splitLongWords=10,
        # allowOrphans=1,
        # spaceBefore=10,
        # spaceAfter=10
        # borderPadding=10,
        # leading=50,
        # spaceAfter=6
    )

    # 将长文本转换为Paragraph对象，以实现自动换行
    for i, row in enumerate(data):
        if i == 0:
            continue
        for j, cell in enumerate(row):
            if isinstance(cell, str) :  # 将所有字符串都处理为Paragraph
               
                data[i][j] = Paragraph(cell, table_paragraph_style)


    # 创建表格对象
    table = Table(data)

    
    # 设置表格样式  # 坐标是先列后行，如(0， -1) 指的是第0列的所有行 
    base_style = [
        
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 设置标题行的文本颜色
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 居中对齐
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), # 上下居中对齐
        
        ('FONTNAME', (0, 0), (-1, -1), 'SunFont'),  # 设置字体
        ('FONTNAME', (0, 0), (-1, len_title - 1), 'SimHei'),  # 黑体的设置长度

        # 设置单元格填充
        # ('LEFTPADDING', (0, 0), (-1, -1), 30),
        # ('RIGHTPADDING', (0, 0), (-1, -1), 30),
        # ('TOPPADDING', (0, 0), (-1, -1), 5),
        # ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        
        # 宽度自动调整
        # ('COLWIDTH', (0, 0), (-1, -1), 'auto')
    ]

    # 所有表格都划线    
    line_style_1 = [   
        ('LINEBEFORE', (0, 0), (-1, -1), 0.5, colors.black),  # 设置左侧竖线（细线）
        ('LINEAFTER', (0, 0), (-1, -1), 0.5, colors.black),  # 设置右侧竖线（细线）
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black),  # 设置所有横线 (细线） 
        ('LINEABOVE', (0, 0), (-1, -1), 0.5, colors.black),  
    ]

    #  三线表
    line_style_2 = [
    ('LINEABOVE', (0, 0), (-1, len_title - 1), 1.5, colors.black),  
    ('LINEBELOW', (0, 0), (-1, len_title - 1), 1.5, colors.black),
    ('LINEBELOW', (0, -1), (-1, -1), 1.5, colors.black),
    ]

    style = base_style + line_style_2 if random.randint(0, 1) == 0 else \
            base_style + line_style_1

    table_style = TableStyle(style)


    for i in range(len_title):  # 多少级header    
        for j in range(header_column_nums):  # 多少列
            if j > 0 and col_names[i][j] == col_names[i][j-1]:
                print(col_names[i][j])
                table_style.add('SPAN', (j-1, i), (j, i))  # 合并列，保留行


    for i in range(len_title):  # 多少级header
        for j in range(header_column_nums):  # 多少列
            if i>0 and col_names[i][j] == col_names[i-1][j]:
                print(col_names[i][j])
                table_style.add('SPAN', (j, i-1), (j, i))  # 合并行，保留列
        

    table.setStyle(table_style)
    

    # 构建 PDF 文档内容
    content = [table]

    # 将内容添加到 PDF 文档中并保存
    doc.build(content)



def add_gaussian_blur(image):
    radius = np.random.randint(5, 13) * 0.1
    noisy_image = image.filter(ImageFilter.GaussianBlur(radius))   # [0.5, 1.2]
    
    return noisy_image


# 均分分布噪声

def add_uniform_noise(image):
    """添加均匀分布噪声"""
    
    img_array = np.array(image)

    
    noise = np.random.uniform(low=0, high=180, size=img_array.shape)
    noisy_img_array = img_array + noise
    noisy_img_array = np.clip(noisy_img_array, 0, 255).astype(np.uint8)
    
    return Image.fromarray(noisy_img_array)

def crop_roi_pad(image, pad_size=5):
   
    
    # 使用argwhere找到所有值为0的元素的索引
    matrix = np.array(image)
    zero_indices = np.argwhere(matrix == 0)
    
    # 计算边界坐标
    min_row, min_col = np.min(zero_indices, axis=0)
    max_row, max_col = np.max(zero_indices, axis=0) + 1  # +1是因为索引是包含的，而裁剪需要开区间
    
    # 确保边界在原矩阵范围内
    min_row, min_col = max(0, min_row), max(0, min_col)
    max_row, max_col = min(matrix.shape[0], max_row), min(matrix.shape[1], max_col)
    
    # 根据边界裁剪矩阵
    roi = matrix[min_row:max_row, min_col:max_col]
    
    padded_roi = np.pad(roi, pad_width=((pad_size, pad_size), 
                                        (pad_size, pad_size)), mode='constant', constant_values=255)
    
    
    return Image.fromarray(padded_roi)
    


def pdf_to_images(pdf_path):
    # 将PDF转换为图片
    # print(pdf_path)
    images = convert_from_path(pdf_path)
    
    if len(images) > 1:  # 如果太长，对于多模态图像识别非常不利
        print('pdf 图像太长: ', pdf_path)
        return 
        
    else:
        image = images[0].convert('L')  # 转为灰度图像
        image = crop_roi_pad(image, pad_size=np.random.randint(50, 200))

        noisy_funcs = [add_uniform_noise, add_gaussian_blur]
        noisy_func = random.choice(noisy_funcs)
        noisy_image = noisy_func(image)
        
        return noisy_image

