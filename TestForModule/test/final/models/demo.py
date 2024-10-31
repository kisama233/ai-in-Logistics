class gpt:
    def __init__(self, name):
        self.name = name

    def get_response(self, prompt):
        # 处理
        prompt = prompt.lower()
        return self.name, prompt


g = gpt("deepseek")
q = input("请输入你的问题：")
text = g.get_response("将问题转换为sql语句，按照如下格式，填空即可，Select * from t where name = <name>，只回复sql语句，其他任何内容都不要回复,问题："+q)

r = g.get_response(q+sjq(text))



