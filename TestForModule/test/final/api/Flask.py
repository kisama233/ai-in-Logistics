import numpy as np
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# 假设你的模型加载和预测函数如下所示
def load_model():
    model_url = 'https://api.deepseek.com'
    model = load_model(model_url)
    return model


def predict(model, parameters):
    # 确保参数的格式符合模型输入的要求
    # 例如，对于Keras模型，通常需要输入为numpy数组
    parameters = np.array(parameters)

    # 使用模型进行预测
    prediction = model.predict(parameters)

    # 返回预测结果
    return prediction

# 假设模型已经加载好了
model = load_model()

@app.route('/')
def index():
    return render_template('index.html')  # 假设你有一个index.html模板


@app.route('/predict', methods=['POST'])
def model_predict():
    # 获取JSON数据
    data = request.get_json(force=True)  #

    # 假设你需要从JSON中获取的参数是'input_data'
    input_data = data.get('input_data')

    # 参数校验，确保所有需要的参数都已经提供
    if input_data is None:
        return jsonify({'error': 'Missing input_data parameter'}), 400

    # 使用模型进行预测
    prediction = predict(model, input_data)

    # 返回预测结果
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)
