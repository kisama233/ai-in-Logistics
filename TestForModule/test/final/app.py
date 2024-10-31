from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import requests
import pymysql
from sqlalchemy import create_engine

app = Flask(__name__)

# GPTStreamer 类定义
class GPTStreamer:
    def __init__(self, gpt_api_key: str, gpt_api_url: str, model: str, stream: bool, system_prompt: str,
                 temperature: float, config: dict, query: str):
        self.GPT_API_KEY = gpt_api_key
        self.GPT_API_URL = gpt_api_url
        self.model = model
        self.stream = stream
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.config = config
        self.data = self.fetch_data_from_cloud_db(query)

    def get_response(self, prompt: list) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.GPT_API_KEY}"
        }

        gpt_data = {
            "model": self.model,
            "messages": prompt,
            "stream": False,
            "temperature": self.temperature
        }

        try:
            response = requests.post(self.GPT_API_URL, headers=headers, json=gpt_data)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
        except KeyError as key_err:
            print(f"Key error in response data: {key_err}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None

    def fetch_data_from_cloud_db(self, query):
        conn_params = self.config
        engine = create_engine(
            f"mysql+pymysql://{conn_params['user']}:{conn_params['password']}@{conn_params['host']}:{conn_params['port']}/{conn_params['db']}")
        try:
            data = pd.read_sql_query(query, engine)
            return data
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    # 新增方法：将对话记录存入数据库
    def send_conversation_log_to_cloud(self, conversation_log):
        conn_params = self.config

        # 建立数据库连接
        try:
            conn = pymysql.connect(
                host=conn_params['host'],
                port=int(conn_params['port']),
                user=conn_params['user'],
                password=conn_params['password'],
                db=conn_params['db'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = conn.cursor()

            # 插入对话数据的 SQL 语句
            insert_query = """
            INSERT INTO conversations (conversation_id, role, message, timestamp)
            VALUES (%s, %s, %s, NOW());
            """

            # 生成对话ID
            conversation_id = f"conv_{pd.Timestamp.now().timestamp()}"

            # 插入对话记录
            for entry in conversation_log:
                cursor.execute(insert_query, (conversation_id, entry['role'], entry['content']))

            # 提交事务
            conn.commit()
            print("对话记录已成功发送到数据库。")

        except pymysql.MySQLError as db_err:
            print(f"Database error occurred: {db_err}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

# 配置文件
config = {
    'host': '1.92.66.96',
    'port': '3306',
    'user': 'mm',
    'password': '123456',
    'db': 'mydatabase'
}

query = "SELECT * FROM data1;"  # 替换为您的实际 SQL 查询
csv_file_path = 'data1.csv'


csv_file_path = 'data1.csv'
df = pd.read_csv(csv_file_path)
print(df)

# 读取CSV文件
df = pd.read_csv(csv_file_path)
df_as_string = df.to_string(index=False)
system_prompt = '你是一个专业的物流信息助手，能够提供关于包裹追踪、运输时效、配送选项、货运费用和物流解决方案的详细信息。你需要使用清晰、准确的术语来回答用户的问题，并始终以友好和专业的态度服务,当用户询问快递途径的地点和预计送达时间时，给出一个具体的流程，并尽量使距离和路途以长距离来回答。'
prompt_with_data = f"{system_prompt}\n以下是物流数据信息：\n{df_as_string}"

gpt_streamer = GPTStreamer(
    gpt_api_key='sk-rGXFKaizSjO3WkJj4439262bCaD345A19d1a93953b66B0A9',  # 替换为你的API密钥
    gpt_api_url='https://a.ltcld.cn/v1/chat/completions',  # 替换为你的API URL
    model='llama-3.2-90b-text-preview',
    stream=True,
    system_prompt=system_prompt,
    temperature=0.7,
    config=config,
    query=query,
)

# 存储对话记录的列表
conversation_log = []

@app.route("/", methods=["GET", "POST"])
def index():
    global conversation_log

    # 读取 CSV 数据作为提示词
    df = pd.read_csv(csv_file_path)
    df_as_string = df.to_string(index=False)
    prompt_with_data = f"{system_prompt}\n以下是物流数据信息：\n{df_as_string}"

    if request.method == "POST":
        user_input = request.form["user_input"]

        # 构建 prompt，包含系统提示词和 CSV 数据
        prompt = [
            {"role": "system", "content": prompt_with_data},
            {"role": "user", "content": user_input}
        ]

        # 获取 GPT 模型的响应
        model_response = gpt_streamer.get_response(prompt)

        # 将用户输入和模型响应保存到对话日志中
        conversation_log.append({"role": "user", "content": user_input})
        conversation_log.append({"role": "assistant", "content": model_response})

        # 将对话记录存储到数据库
        gpt_streamer.send_conversation_log_to_cloud(conversation_log)

        return redirect(url_for("index"))

    return render_template("chat.html", conversation_log=conversation_log)


if __name__ == "__main__":
    app.run(debug=True)
