# import pandas as pd
# import requests
# import pymysql
# from sqlalchemy import create_engine
#
#
# class GPTStreamer:
#     def __init__(self, gpt_api_key: str, gpt_api_url: str, model: str, stream: bool, system_prompt: str,
#                  temperature: float, config: dict, query: str):
#         self.GPT_API_KEY = gpt_api_key
#         self.GPT_API_URL = gpt_api_url
#         self.model = model
#         self.stream = stream
#         self.system_prompt = system_prompt
#         self.temperature = temperature
#         self.config = config
#         self.data = self.fetch_data_from_cloud_db(query)
#
#
#     def get_response(self, prompt: list) -> str:
#         headers = {
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer {self.GPT_API_KEY}"
#         }
#
#         gpt_data = {
#             "model": self.model,
#             "messages": prompt,
#             "stream": False,
#             "temperature": self.temperature
#         }
#
#         try:
#             response = requests.post(self.GPT_API_URL, headers=headers, json=gpt_data)
#             response.raise_for_status()
#             return response.json()['choices'][0]['message']['content']
#         except requests.exceptions.HTTPError as http_err:
#             print(f"HTTP error occurred: {http_err}")
#         except requests.exceptions.ConnectionError as conn_err:
#             print(f"Connection error occurred: {conn_err}")
#         except requests.exceptions.Timeout as timeout_err:
#             print(f"Timeout error occurred: {timeout_err}")
#         except requests.exceptions.RequestException as req_err:
#             print(f"An error occurred: {req_err}")
#         except KeyError as key_err:
#             print(f"Key error in response data: {key_err}")
#         except Exception as e:
#             print(f"An unexpected error occurred: {e}")
#         return None
#
#
#     def interact_with_user(self):
#         print("开始与用户对话，输入'exit'退出。")
#         conversation_log = []  # 初始化对话日志列表
#         while True:
#             user_input = input("用户: ")
#             if user_input.lower() == 'exit':
#                 print("对话结束。")
#                 break
#
#             prompt = [{"role": "system", "content": self.system_prompt}, {"role": "user", "content": user_input}]
#             print("正在生成响应...")
#             response = self.get_response(prompt)  # 获取模型的响应
#             if response:
#                 print(f"模型: {response}")
#                 # 将用户输入和模型响应添加到对话日志中
#                 conversation_log.append({"prompt": user_input, "response": response})
#
#         # 对话结束后，将整个对话日志发送到云端数据库
#         self.send_conversation_log_to_cloud(conversation_log)
#     # def interact_with_user(self):
#     #     print("开始与用户对话，输入'exit'退出。")
#     #     conversation_log = []  # 初始化对话日志列表
#     #     while True:
#     #         user_input = input("用户: ")
#     #         if user_input.lower() == 'exit':
#     #             print("对话结束。")
#     #             break
#     #
#     #         try:
#     #             # 生成 SQL 语句
#     #             sql_prompt = ("将问题转换为sql语句，按照如下格式，填空即可，Select * from t where name = '<name>'，只回复sql语句，其他任何内容都不要回复,问题：" + user_input)
#     #             sql_prompt = "".join(sql_prompt)
#     #             sql_response = gpt_streamer.get_response(sql_prompt,'李伟')
#     #
#     #             if sql_response:
#     #                 # 执行 SQL 语句
#     #                 sql_result = self.execute_sql(sql_response)
#     #
#     #                 # 根据 SQL 结果生成回答
#     #                 if sql_result:
#     #                     answer = f"根据您的问题，查询到的结果是：{sql_result}"
#     #                 else:
#     #                     answer = "很抱歉，根据您的问题，没有查询到相关结果。"
#     #             else:
#     #                 answer = "未能生成有效的 SQL 语句。"
#     #
#     #             print(f"模型: {answer}")
#     #             conversation_log.append({"prompt": user_input, "response": answer})
#     #
#     #         except TypeError as e:
#     #             print("类型错误:", e)
#     #         except Exception as e:
#     #             print("发生了一个错误:", e)
#     #
#     #     # 对话结束后，将整个对话日志发送到云端数据库
#     #     self.send_conversation_log_to_cloud(conversation_log)
#
#     def process_model_response(self, model_response):
#         # 假设 model_response 是一个列表，其中包含多个字典，每个字典代表一条记录
#         for record in model_response:
#             print(f"处理模型返回的数据：{record}")
#             # 这里可以添加代码来进一步处理每条记录
#
#         # 输出与模型的对话
#         for conversation in model_response:
#             print(f"用户: {conversation['prompt']}")
#             print(f"模型: {conversation['response']}")
#
#     def send_conversation_to_cloud(self, conversation):
#         # 云数据库连接配置
#         conn_params = self.config  # 假设config已经作为类属性
#
#         # 建立数据库连接
#         try:
#             conn = pymysql.connect(host=conn_params['host'],
#                                    port=int(conn_params['port']),
#                                    user=conn_params['user'],
#                                    password=conn_params['password'],
#                                    db=conn_params['db'],
#                                    charset='utf8mb4',
#                                    cursorclass=pymysql.cursors.DictCursor)
#             cursor = conn.cursor()
#
#             # 插入对话数据
#             insert_query = """
#             INSERT INTO recognized_texts (conversation_id, role, message)
#             VALUES (%s, %s, %s);
#             """
#
#             # 假设 `conversation_id` 是唯一标识对话的字符串
#             conversation_id = 'conv_12345'
#
#             # 插入用户的消息
#             cursor.execute(insert_query, (conversation_id, 'user', conversation['prompt']))
#
#             # 插入模型的消息
#             cursor.execute(insert_query, (conversation_id, 'assistant', conversation['response']))
#
#             # 提交事务
#             conn.commit()
#             print("完整的对话数据已成功发送到云端数据库。")
#
#         except pymysql.MySQLError as db_err:
#             print(f"Database error occurred: {db_err}")
#         except Exception as e:
#             print(f"An unexpected error occurred: {e}")
#         finally:
#             # 关闭游标和连接
#             if cursor:
#                 cursor.close()
#             if conn:
#                 conn.close()
#
#     def send_data_to_cloud(self, dataset):
#         # 云数据库连接配置
#         conn_params = self.config  # 假设config已经作为类属性
#
#         # 建立数据库连接
#         try:
#             conn = pymysql.connect(host=conn_params['host'],
#                                    port=int(conn_params['port']),
#                                    user=conn_params['user'],
#                                    password=conn_params['password'],
#                                    db=conn_params['db'],
#                                    charset='utf8mb4',
#                                    cursorclass=pymysql.cursors.DictCursor)
#             cursor = conn.cursor()
#
#             # 插入数据集数据
#             insert_query = """
#             INSERT INTO recognized_texts (name, code_gender, phone, address)
#             VALUES (%s, %s, %s, %s);
#             """
#
#             # 执行批量插入
#             for record in dataset:
#                 cursor.execute(insert_query,
#                                (record['name'], record['code_gender'], record['phone'], record['address']))
#
#             # 提交事务
#             conn.commit()
#             print("数据集已成功发送到云端数据库。")
#
#         except pymysql.MySQLError as db_err:
#             print(f"Database error occurred: {db_err}")
#         except Exception as e:
#             print(f"An unexpected error occurred: {e}")
#         finally:
#             # 关闭游标和连接
#             if cursor:
#                 cursor.close()
#             if conn:
#                 conn.close()
#
#     def send_conversation_log_to_cloud(self, conversation_log):
#         # 云数据库连接配置
#         conn_params = self.config  # 假设config已经作为类属性
#
#         # 建立数据库连接
#         try:
#             conn = pymysql.connect(host=conn_params['host'],
#                                    port=int(conn_params['port']),
#                                    user=conn_params['user'],
#                                    password=conn_params['password'],
#                                    db=conn_params['db'],
#                                    charset='utf8mb4',
#                                    cursorclass=pymysql.cursors.DictCursor)
#             cursor = conn.cursor()
#
#             # 插入对话数据
#             insert_query = """
#             INSERT INTO recognized_texts (conversation_id, role, message)
#             VALUES (%s, %s, %s);
#             """
#
#             # 假设 `conversation_id` 是唯一标识对话的字符串
#             conversation_id = 'conv_{}'.format(int(pd.Timestamp.now().timestamp()))
#
#             for entry in conversation_log:
#                 # 插入用户的消息
#                 cursor.execute(insert_query, (conversation_id, 'user', entry['prompt']))
#                 # 插入模型的消息
#                 cursor.execute(insert_query, (conversation_id, 'assistant', entry['response']))
#
#             # 提交事务
#             conn.commit()
#             print("完整的对话数据已成功发送到云端数据库。")
#
#         except pymysql.MySQLError as db_err:
#             print(f"Database error occurred: {db_err}")
#         except Exception as e:
#             print(f"An unexpected error occurred: {e}")
#         finally:
#             # 关闭游标和连接
#             if cursor:
#                 cursor.close()
#             if conn:
#                 conn.close()
#
#     def fetch_data_from_cloud_db(self, query):
#         # 云数据库连接配置
#         conn_params = self.config  # 假设config已经作为类属性
#
#         # 创建SQLAlchemy引擎
#         engine = create_engine(
#             f"mysql+pymysql://{conn_params['user']}:{conn_params['password']}@{conn_params['host']}:{conn_params['port']}/{conn_params['db']}")
#
#         # 使用SQLAlchemy引擎执行查询
#         try:
#             data = pd.read_sql_query(query, engine)
#             return data
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             return None
#         finally:
#             # SQLAlchemy引擎不需要显式关闭连接
#             pass
#
#
# config = {
#     'host': '1.92.66.96',
#     'port': '3306',
#     'user': 'mm',
#     'password': '123456',
#     'db': 'mydatabase'
# }
#
# # query = "SELECT * FROM recognized_texts;"
# query = "SELECT * FROM data1;"  # 替换为您的实际 SQL 查询
#
# # 读取CSV文件
# csv_file_path = 'data1.csv'
# df = pd.read_csv(csv_file_path)
# print(df)
# df_as_string = df.to_string(index=False)
# system_prompt = '你是一个专业的物流信息助手，能够提供关于包裹追踪、运输时效、配送选项、货运费用和物流解决方案的详细信息。你需要使用清晰、准确的术语来回答用户的问题，并始终以友好和专业的态度服务。'
# prompt_with_data = f"{system_prompt}\n以下是物流数据信息：\n{df_as_string}"
#
#
#
#
# # 实例化 GPTStreamer 类
# gpt_streamer = GPTStreamer(
#     gpt_api_key='sk-4baee077701947a1a912192679bcc6bc',  # 替换为你的API密钥
#     gpt_api_url='https://api.deepseek.com/chat/completions',  # 替换为你的API URL
#     model='deepseek-chat',
#     stream=True,
#     system_prompt=system_prompt+df_as_string,
#     temperature=0.7,
#     config=config,
#     query=query,  # 传入查询参数
#
# )
#
# # g = GPTStreamer("李四")
# # question = input("请输入你的问题")
# # text = gpt_streamer.get_response(
# #     "将问题转换为sql语句，按照如下格式，填空即可，Select * from t where name = <name>，只回复sql语句，其他任何内容都不要回复,问题：" + question)
# # r = gpt_streamer.get_response(question + (text))
# # question = input("请输入你的问题")
# # try:
# #     text = gpt_streamer.get_response(
# #         "将问题转换为sql语句，按照如下格式，填空即可，Select * from t where name = <name>，只回复sql语句，其他任何内容都不要回复,问题：" + question)
# #     if text is not None:
# #         full_question = question + text
# #         r = gpt_streamer.get_response(full_question)
# #     else:
# #         print("未能生成有效的 SQL 语句。")
# # except TypeError as e:
# #     print("类型错误:", e)
# # except Exception as e:
# #     print("发生了一个错误:", e)
# # #
# # 开始与用户对话
# gpt_streamer.interact_with_user()
#
# received_data_from_model = [
#
#     {'name': '刘伟', 'code_gender': '女', 'phone': '13654417153', 'address': ' 南京市秦淮区'},
#
# ]
#
# # 发送从模型接收到的数据集到云端
# gpt_streamer.send_data_to_cloud(received_data_from_model)
#
# conversation_with_model = {
#     'prompt': '用户: 你好，我想查询包裹状态。',
#     'response': '模型: 您好，请提供您的包裹追踪号码。'
# }
#
# # 发送与模型的对话内容到云端
# gpt_streamer.send_conversation_to_cloud(conversation_with_model)
