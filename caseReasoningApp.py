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


@app.route('/caseReasoning', methods=['GET', "POST"])
def reasoning():
    """
    step1: 获取参数，包括研究区范围&应用场景（例如dsm）&土壤空间推测需要的属性,测试下先用模拟数据
    step2: 计算研究区的地理环境特征（案例化）
    step3：根据案例化的结果进行案例推理（原型方法）

    :return: 返回推荐的参数
    """
    # 分治的时候要做好基本问题的形式化
    data = request.get_data(as_text=True)
    json_data = json.loads(data)
    # print(json_data)
    # 测试数据
    # area_hs = ["125.15", "125.27", "48.99", "48.88"]
    # area_xc = ["118.5", "119.6", "31.3", "30.6"]
    # area_zxh = ["116.4", "116.5", "25.7", "25.63"]
    # json_data = {"studyArea": area_hs,
    #              "arg": {"up": "0", "down": "40", "property": "SOM"}, "model": "iPSM"}

    # Load the YAML config file containing the property codes
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # Replace the property value with its code from the YAML config file
    json_data['arg']['property'] = str(config['property_codes'][json_data['arg']['property']])

    json_demo = convert_value(json_data)
    scenario, result = crm.caseParsing(json_demo)
    print(scenario)
    print(result)
    return jsonify(result)


@app.route('/caseReasoningEGC', methods=['GET', "POST"])
def reasoningEGC():
    """
    step1: 获取参数，包括研究区范围&应用场景（例如dsm）&土壤空间推测需要的属性,测试下先用模拟数据
    step2: 计算研究区的地理环境特征（案例化）
    step3：根据案例化的结果进行案例推理（原型方法）

    :return: 返回推荐的参数
    """
    #
    data = request.get_data(as_text=True)
    json_data = json.loads(data)
    # print(json_data)
    # 测试数据
    # area_hs = ["125.15", "125.27", "48.99", "48.88"]
    # area_xc = ["118.5", "119.6", "31.3", "30.6"]
    # area_zxh = ["116.4", "116.5", "25.7", "25.63"]
    # json_data = {"studyArea": ["125.15", "48.99"],
    #             "arg": {"up": "0", "down": "40", "property": "SOM"}, "model": "iPSM"}
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # Replace the property value with its code from the YAML config file
    json_data['arg']['property'] = str(config['property_codes'][json_data['arg']['property']])

    json_demo = convert_value(json_data)
    result = crm.caseParsingEGC(json_demo)
    data = result['most_similiar_case']['covariates']
    new_covariates = []
    for covariate in data:
        new_covariate = ''
        for word in covariate.split('_'):
            new_word = word.capitalize()
            if 'dem' in new_word.lower():
                new_word = new_word.replace('Dem', 'DEM')
            new_covariate += new_word + '_'
        new_covariates.append(new_covariate[:-1])
    jsonresult = {}
    jsonresult['covariates'] = new_covariates
    return jsonify(jsonresult)


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=7511)
    # app.run()
