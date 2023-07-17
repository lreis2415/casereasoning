from flask import Flask, request, jsonify
from waitress import serve
import json
import CaseReasonmingMethod as crm

app = Flask(__name__)
# app.debug = True


@app.route('/')
def start():  # put application's code here
    return "The program is running!"

@app.route('/caseReasoning',methods=['GET',"POST"])
def reasoning():
    """
    step1: 获取参数，包括研究区范围&应用场景（例如dsm）&土壤空间推测需要的属性,测试下先用模拟数据
    step2: 计算研究区的地理环境特征（案例化）
    step3：根据案例化的结果进行案例推理（原型方法）

    :return: 返回推荐的参数
    """
    #
    # data = request.get_data(as_text=True)
    # json_data = json.loads(data)
    # 测试数据
    json_data = {'studyArea': ['680400', '752100', '3415000', '3382000'], 'arg': {'up': '6', 'down': '20', 'property': '15'}, 'model': 'iPSM'}
    # json_demo = {"studyArea": [680400, 752100, 3415000, 3382000], "model": "DSM", "arg": [{"up": 6, "down": 20, "property": 15}]}
    # 输入推理任务+数据字典，返回推荐的结果

    result = crm.caseParsing(json_data)

    return jsonify(result)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=7511)
    #app.run()

