from flask import Flask, request
from waitress import serve

app = Flask(__name__)
app.debug = True


@app.route('/')
def start():  # put application's code here
    return "The program is running!"

@app.route('/caseReasoning',methods=['GET',"POST"])
def reasoning():
    """
    step1: 获取参数，包括研究区范围&带推测的土壤属性（可能按规则推测）,测试下先用模拟数据
    step2: 计算研究区的地理环境特征（案例化）
    step3：根据案例化的结果进行案例推理（原型方法）

    :return: 返回推荐的参数
    """



if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=7581)
    # app.run()
