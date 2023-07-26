from flask import Flask, request, jsonify
from waitress import serve
import json
import CaseReasonmingMethod as crm
import yaml

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
    area_hs = ["13930938.8046", "13944803.5628", "6272610.1266", "6255945.02208"]
    area_xc = ["13187337.5493", "13319340.7388", "3673702.02484", "3573518.21994"]
    json_data = {"studyArea": area_xc,
                 "arg": {"up": "0", "down": "40", "property": "SOM"}, "model": "iPSM"}

    # Load the YAML config file containing the property codes
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # Replace the property value with its code from the YAML config file
    json_data['arg']['property'] = str(config['property_codes'][json_data['arg']['property']])

    json_demo = convert_value(json_data)
    result = crm.caseParsing(json_demo)
    return jsonify(result)

if __name__ == '__main__':
    print('run')
    serve(app, host='0.0.0.0', port=7511)
    #app.run()
