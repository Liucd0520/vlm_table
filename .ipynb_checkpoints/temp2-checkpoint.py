from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# 注册中文字体
pdfmetrics.registerFont(TTFont('SimSun', 'SimSun.ttf'))

# 创建 PDF 文件
pdf = SimpleDocTemplate("example.pdf", pagesize=letter)

# 获取样式
styles = getSampleStyleSheet()

# 创建一个新的段落样式，使用注册的中文字体
# style = ParagraphStyle(
#     name='SimSun',
#     parent=styles['Normal'],
#     fontName='SimSun',
#     fontSize=10,
#     leading=14
# )

   # 自定义一个段落样式来处理表格中的文本，也就是处理行长文本的问题
style = ParagraphStyle(
        'table_paragraph',
        # parent=styles['Normal'],
        fontName='SimSun',
        # wordWrap='CJK',
        # splitLongWords=10,
        # allowOrphans=1,
        # spaceBefore=10,
        # spaceAfter=10
        # borderPadding=10,
        # leading=50,
        # spaceAfter=6
    )

# 准备表格数据
# data = [
#     ['Header 1', 'Header 2', 'Header 3'],
#     ['这是一个很长的文本，用来测试自长的文本，用来测试自动换行长的文本，用来测试自动换行动换行和，用来测试自动换行和宽度自适应', '短文本', '中等长度的文本'],
#     ['短文本', '这是另一个较长的文本，用来测试表格列宽的自动调整', '再次测试']
# ]

data = [
    ['旗帜', '日期', '名称', '性质', '设计与涵义'],
 ['',  '1219年6月15日',  '丹麦王国国旗',  '',  '比例28:37。红底白十字的旗帜，是世界上最古老的国旗。据丹麦史诗，在中世纪时1219年丹麦国王瓦尔德马二世（Valdemar II）受教宗之托远征爱沙尼亚。丹麦军队原本苦战受挫，但是当时从天空降下此旗，之后丹麦军队获得了胜利，最后该旗成为国旗。另说该旗是教宗送给的旗帜，代表教宗的支持。'],
 ['',  '1821年7月13日',  '挪威王国国旗',  '',  '比例8:11。红底白边蓝十字的旗帜。红色、白色与蓝色象征自由、平等、博爱。该旗以丹麦国旗为基本图案，结合美国星条旗和法国三色旗的色彩，在红底白十字中加入蓝色十字。'],
#  ['',  '1905年6月7日',  '瑞典王国国旗',  '',  '比例5:8。蓝底黄十字的旗帜。金十字代表瑞典福尔孔王朝中的金色十字架。1157年瑞典国王埃里克九世于远征芬兰前向神祷告，突然看到如同金色十字架的光芒横越青空，后来成为现在的国旗。'],
 ['',  '1915年6月19日', '冰岛共和国国旗',  '',  '比例18:25。蓝底白边红十字的旗帜。蓝色代表海水，也是冰岛的传统服饰。白色代表冰岛的雪原与冰河，红色代表冰岛的火山与地热。'],
#  ['',  '1918年5月29日',  '芬兰共和国国旗',  '',  '比例11:18。白底蓝十字的旗帜。蓝色代表湖与天，白色代表雪。其中斯堪的纳维亚十字源自与瑞典的关系，蓝色与白色的颜色则是源自俄国沙皇的颜色。']
  ]



# 将长文本转换为Paragraph对象，以实现自动换行
for i, row in enumerate(data):
    if i == 0:
        continue
    for j, cell in enumerate(row):
        if isinstance(cell, str) :  # 将所有字符串都处理为Paragraph
            print(cell)
            data[i][j] = Paragraph(cell, style)


# # 动态计算列宽
# col_widths = [0] * len(data[0])
# for row in data:
#     for i, cell in enumerate(row):
#         if isinstance(cell, Paragraph):
#             para_width, _ = cell.wrap(0, 0)
#             col_widths[i] = max(col_widths[i], para_width)
#         else:
#             col_widths[i] = max(col_widths[i], len(cell) * style.fontSize)

# print(col_widths)
# 创建表格并设置样式
table = Table(data, colWidths=[30, 100, 100, 30, 300])

table.setStyle(TableStyle(
    # [
    # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    # ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    # ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    # ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
    # ]
 [
        
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 设置标题行的文本颜色
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 居中对齐
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), # 上下居中对齐
        
        ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),  # 设置字体
        ('FONTNAME', (0, 0), (-1, 1), 'SimSun'),  # 黑体的设置长度

        # 设置单元格填充
        # ('LEFTPADDING', (0, 0), (-1, -1), 30),
        # ('RIGHTPADDING', (0, 0), (-1, -1), 30),
        # ('TOPPADDING', (0, 0), (-1, -1), 5),
        # ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        
        # 宽度自动调整
        # ('COLWIDTH', (0, 0), (-1, -1), 'auto')
    ]
))

# 构建 PDF
elements = [table]
pdf.build(elements)

print("PDF 生成成功")
