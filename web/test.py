# -*- coding: utf-8 -*-
import json


def main(body) -> dict:
    data = json.loads(body)
    return {
        "success": 'true' if data['code'] == 200 else 'false'
    }

def transform_question(question, index):
    common_fields = {
        "field": f"data{index}",
        "showIndex": True,
        "showType": True,
        "showSpliter": True,
        "isRequired": True,
        "randomSort": False,
        "showLeftNum": True,
        "innerRandom": False,
        "checked": False,
        "selectType": "radio",
        "sortWay": "v",
        "noNps": "",
        "minNum": "",
        "maxNum": "",
        "starStyle": "star",
        "starMin": 1,
        "starMax": 5,
        "min": 0,
        "max": 10,
        "minMsg": "",
        "maxMsg": "",
        "rangeConfig": {},
        "star": 5,
        "optionOrigin": "",
        "originType": "selected",
        "matrixOptionsRely": "",
        "numberRange": {
            "min": {
                "placeholder": "0",
                "value": 0
            },
            "max": {
                "placeholder": "1000",
                "value": 1000
            }
        },
        "textRange": {
            "min": {
                "placeholder": "0",
                "value": 0
            },
            "max": {
                "placeholder": "500",
                "value": 500
            }
        },
        "isSelected": False,
        "indexNumber": index + 1,
        "qIndex": index
    }

    if question['type'] == 'textarea':
        return {
            **common_fields,
            "type": "textarea",
            "title": f"<p>{question['title']}</p>",
            "placeholder": question['placeholder'],
        }
    elif question['type'] == 'radio':
        options = [{
            "text": opt['text'],
            "others": opt.get('others', False),
            "placeholderDesc": opt.get('placeholderDesc', ""),
        } for opt in question['options']]
        return {
            **common_fields,
            "type": "radio",
            "title": question['title'],
            "options": options,
        }
    elif question['type'] == 'checkbox':
        options = [{
            "text": opt['text'],
            "others": opt.get('others', False),
            "placeholderDesc": opt.get('placeholderDesc', ""),
        } for opt in question['options']]
        return {
            **common_fields,
            "type": "checkbox",
            "title": question['title'],
            "options": options,
        }
    elif question['type'] == 'radio-nps':
        return {
            **common_fields,
            "type": "radio-nps",
            "title": question['title'],
            "min": question.get('min', 0),
            "max": question.get('max', 10),
            "minMsg": question.get('minMsg', '极不满意'),
            "maxMsg": question.get('maxMsg', '十分满意'),
        }
    else:
        raise ValueError(f"Unknown question type: {question['type']}")


def parse(qjson: str) -> dict:
    questions = json.loads(qjson)
    return [transform_question(q, i) for i, q in enumerate(questions)]

def outputCompletData(surveryId, title, description, dataList):
    return {
  "surveyId": surveryId,
  "configData": {
    "bannerConf": {
      "titleConfig": {
        "mainTitle": title,
        "subTitle": description
      },
      "bannerConfig": {
        "bgImage": "/imgs/skin/17e06b7604a007e1d3e1453b9ddadc3c.webp",
        "bgImageAllowJump": False,
        "bgImageJumpLink": "",
        "videoLink": "",
        "postImg": ""
      }
    },
    "baseConf": {
      "begTime": "2024-07-15 17:31:56",
      "endTime": "2034-07-15 17:31:56",
      "language": "chinese",
      "showVoteProcess": "allow",
      "tLimit": 0,
      "answerBegTime": "00:00:00",
      "answerEndTime": "23:59:59",
      "answerLimitTime": 0
    },
    "bottomConf": {
      "logoImage": "/imgs/Logo.webp",
      "logoImageWidth": "60%"
    },
    "skinConf": {
      "backgroundConf": {
        "color": "#fff"
      },
      "themeConf": {
        "color": "#1677ff"
      },
      "contentConf": {
        "opacity": 100
      },
      "skinColor": "#4a4c5b",
      "inputBgColor": "#ffffff"
    },
    "submitConf": {
      "submitTitle": "提交",
      "msgContent": {
        "msg_200": "提交成功",
        "msg_9001": "您来晚了，感谢支持问卷~",
        "msg_9002": "请勿多次提交！",
        "msg_9003": "您来晚了，已经满额！",
        "msg_9004": "提交失败！"
      },
      "confirmAgain": {
        "is_again": True,
        "again_text": "确认要提交吗？"
      },
      "link": ""
    },
    "dataConf": {
      "dataList": dataList
    }
  }
}

def main(surveryId: str, title: str, description: str, qjson:str) -> dict:
    dataList = parse(qjson)
    reqData = outputCompletData(surveryId, title, description, dataList)

    return json.dumps(reqData, ensure_ascii=False, indent=2)

print(main("123", '1234132', '1234324', '[\n  {\n    \"type\": \"textarea\",\n    \"title\": \"您认为灰色长裤销量不佳的可能原因是什么？\",\n    \"placeholder\": \"请详细描述您的看法。\"\n  },\n  {\n    \"type\": \"radio\",\n    \"title\": \"您认为灰色长裤的定价是否合理？\",\n    \"options\": [\n      {\n        \"text\": \"合理\",\n        \"others\": false\n      },\n      {\n        \"text\": \"偏高\",\n        \"others\": false\n      },\n      {\n        \"text\": \"偏低\",\n        \"others\": false\n      }\n    ]\n  },\n  {\n    \"type\": \"checkbox\",\n    \"title\": \"您认为灰色长裤在哪些方面需要改进？\",\n    \"options\": [\n      {\n        \"text\": \"材质\",\n        \"others\": false\n      },\n      {\n        \"text\": \"设计\",\n        \"others\": false\n      },\n      {\n        \"text\": \"尺码\",\n        \"others\": false\n      },\n      {\n        \"text\": \"包装\",\n        \"others\": false\n      },\n      {\n        \"text\": \"其他\",\n        \"others\": true,\n        \"placeholderDesc\": \"请具体说明\"\n      }\n    ]\n  },\n  {\n    \"type\": \"radio-nps\",\n    \"title\": \"您对灰色长裤的舒适度评价如何？\",\n    \"min\": 0,\n    \"minMsg\": \"极不满意\",\n    \"max\": 10,\n    \"maxMsg\": \"非常满意\"\n  }\n]'))