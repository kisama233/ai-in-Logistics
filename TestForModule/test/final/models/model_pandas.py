# 模型Pandas的实现


import pandas as pd

# 读取文件
df = pd.read_csv('../data1.csv')
# df1 = pd.read_excel('data.xlsx')
# df2 = pd.read_json('data.json')
# # df3 = pd.read_sql('SELECT * FROM table', con=engine)
# df4 = pd.read_hdf('data.h5', 'key')
# # 查看数据前几行
print(df.head())

# # 转换列的数据类型
# df['price'] = df['price'].astype(float)
# df['date'] = pd.to_datetime(df['date'])

# # 假设有一个函数，将价格增加10%
# def increase_price(row):
#     return row['price'] * 1.10
#
# # 应用函数转换
# df['new_price'] = df.apply(increase_price, axis=1)
#
# # 保存转换后的数据到新的CSV文件
# df.to_csv('data_transformed.csv', index=False)
#


#举例

# 读取CSV文件
df = pd.read_csv('../data1.csv')

# 将DataFrame转换为JSON格式的字符串
json_str = df.to_json(orient='records')
print(json_str)
# # 如果你想将JSON字符串保存到文件中，可以这样做：
# with open('data.json', 'w') as json_file:
#     json_file.write(json_str)


# import pandas as pd
#
# # 读取TXT文件，假设字段是用逗号分隔的
# df = pd.read_table('data.txt', sep=',')
#
# # 将DataFrame转换为JSON格式的字符串
# json_str = df.to_json(orient='records')
#
# # 将JSON字符串保存到文件中
# with open('data.json', 'w') as json_file:
#     json_file.write(json_str)
