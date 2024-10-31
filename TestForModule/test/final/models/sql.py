import pymysql

# 数据库连接配置
db_config = {
    'host': '1.92.66.96',  # 替换为你的 MySQL 主机名或 IP 地址
    'port': 3306,  # MySQL 端口号
    'user': 'mm',  # MySQL 用户名
    'password': '123456',  # MySQL 密码
    'db': 'mydatabase',  # 目标数据库名称
    'charset': 'utf8mb4'  # 设置字符集
}

# 创建表的 SQL 语句
create_table_query = """
CREATE TABLE IF NOT EXISTS conversations (
    conversation_id VARCHAR(255) NOT NULL,
    role ENUM('user', 'assistant') NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

# 插入示例数据的 SQL 语句
insert_data_query = """
INSERT INTO conversations (conversation_id, role, message) 
VALUES (%s, %s, %s);
"""

# 示例数据
conversation_data = [
    ('conv_12345', 'user', '你好，物流信息是什么？'),
    ('conv_12345', 'assistant', '你好，我可以为你提供物流信息，请问你需要查询什么？'),
    ('conv_12345', 'user', '请查询我的包裹状态。'),
    ('conv_12345', 'assistant', '你的包裹在途中，将于明天送达。')
]

# 连接数据库并执行 SQL 语句
try:
    # 连接到 MySQL 数据库
    connection = pymysql.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        db=db_config['db'],
        charset=db_config['charset'],
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        # 创建 conversations 表
        cursor.execute(create_table_query)
        print("Table 'conversations' created or already exists.")

        # 插入示例对话数据
        cursor.executemany(insert_data_query, conversation_data)
        print("Sample conversation data inserted successfully.")

    # 提交事务
    connection.commit()

except pymysql.MySQLError as e:
    print(f"Error occurred: {e}")
finally:
    # 关闭数据库连接
    if connection:
        connection.close()
        print("Database connection closed.")


# import pandas as pd
# from sqlalchemy import create_engine
# from sqlalchemy.exc import OperationalError
#
# # 数据库连接配置
# config = {
#     'host': '1.92.66.96',
#     'port': '3306',
#     'user': 'mm',
#     'password': '123456',
#     'db': 'mydatabase'  # 指定要连接的数据库名称
# }
#
# # 使用 SQLAlchemy 创建连接引擎，不指定数据库名称
# engine = create_engine(f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}")
#
# # 尝试创建数据库
# try:
#     with engine.connect() as conn:
#         conn.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
#         print("Database 'mydatabase' created successfully.")
# except OperationalError as e:
#     print(f"Error creating database: {e}")
#
# # 修改连接引擎以连接到新创建的数据库
# engine = create_engine(f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}/{config['db']}")
#
# # 尝试创建表
# try:
#     with engine.connect() as conn:
#         # 创建表
#         create_table_query = """
#         CREATE TABLE IF NOT EXISTS recognized (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(255) NOT NULL,
#             timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         )
#         """
#         conn.execute(create_table_query)
#         print("Table 'recognized' created successfully.")
# except OperationalError as e:
#     print(f"Error creating table: {e}")
#
# # 执行查询以获取数据（假设表已经存在）
# try:
#     query_sql = "SELECT * FROM recognized;"  # 确保表名正确
#     df = pd.read_sql(query_sql, engine)
#
#     # 将DataFrame保存为CSV文件
#     csv_file_path = 'recognized.csv'
#     df.to_csv(csv_file_path, index=False)
#     print(f"Data saved to {csv_file_path}")
#
# except Exception as e:
#     print(f"Error: {e}")
