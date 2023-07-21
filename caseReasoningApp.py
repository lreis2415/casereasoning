from flask import Flask, request, jsonify
from waitress import serve
import json
import CaseReasonmingMethod as crm

app = Flask(__name__)
app.debug = True

@app.route('/')
def start():  # put application's code here
    return "The program is running!"
def convert_value(value):
    if isinstance(value, str):
        if value.isdigit():
            return int(value)
        else:
            try:
                return float(value)
            except ValueError:
                return value
    elif isinstance(value, list):
        return [convert_value(x) for x in value]
    elif isinstance(value, dict):
        return {k: convert_value(v) for k, v in value.items()}
    else:
        return value

@app.route('/caseReasoning',methods=['GET',"POST"])
def reasoning():
    """
    step1: 获取参数，包括研究区范围&应用场景（例如dsm）&土壤空间推测需要的属性,测试下先用模拟数据
    step2: 计算研究区的地理环境特征（案例化）
    step3：根据案例化的结果进行案例推理（原型方法）

    :return: 返回推荐的参数
    """
    #
    #data = request.get_data(as_text=True)
    #json_data = json.loads(data)
    # 测试数据
    json_data = {"studyArea": ["680400", "752100", "3415000", "3382000"],
                 "arg": {"up": "6", "down": "20", "property": "15"}, "model": "iPSM"}
    json_demo = convert_value(json_data)
    result = crm.caseParsing(json_demo)
    return jsonify(result)

if __name__ == '__main__':
    print('run')
    serve(app, host='0.0.0.0', port=7511)
    #app.run()

