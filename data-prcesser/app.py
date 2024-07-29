from flask import Flask, request, jsonify
from datetime import datetime
import psycopg2
import json
import json_repair
from collections import defaultdict
import asyncio
import aiohttp

# 数据库连接配置
conn = psycopg2.connect(
    dbname="commerce",
    user="postgres",
    password="difyai123456",
    host="10.201.0.212",
    port="5433"
)
cursor = conn.cursor()

app = Flask(__name__)


async def request_agent_flow_block(session, token, query, inputs):
    NLP_URL = "https://fastcopilot.deepexi.com/v1/chat-messages"
    try:
        async with session.post(
            url=NLP_URL,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={
                "user": "plc",
                "query": query,
                "inputs": inputs,
                "response_mode": "blocking"
            }
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data['answer']
        
    except aiohttp.ClientError as e:
        print(f"An error occurred: {e}")
        return None


async def nlp_process(survey_id):
    # 从数据库获取全部文本输入数据
    cursor.execute("""
        SELECT value_text FROM survey_responses
        where value_type = 'text'
        and survey_id = %s
    """, (survey_id,))
    rows = cursor.fetchall()
    # 生成NLP语料
    all_text = '\n'.join([row[0] for row in rows])

    # 从数据库获取题目的输入数据
    cursor.execute("""
        SELECT question_id, value_text FROM survey_responses
        where survey_id = %s
        and value_text is not  null
    """, (survey_id,))
    rows = cursor.fetchall()
    # 生成NLP语料
    questions = defaultdict(list)
    for row in rows:
        question_id, value_text = row
        questions[question_id].append(value_text)

    
    # NLP处理
    async with aiohttp.ClientSession() as session:
        
        tasks = []
        sentiment_req = request_agent_flow_block(session, 
                                                          token='app-uVXUmnxqocXaMfVU32ZXiUkd', 
                                                          query=all_text, 
                                                          inputs={"type": "情感总结"})
        tasks.append(sentiment_req)

        for question_id, value_texts in questions.items():
            topic_req = request_agent_flow_block(session, 
                                                        token='app-uVXUmnxqocXaMfVU32ZXiUkd', 
                                                        query='\n'.join(value_texts), 
                                                        inputs={"type": "主题分析"})
            tasks.append(topic_req)
        
        results = await asyncio.gather(*tasks)

    print(results)
    sentiment = json_repair.loads(results[0])
    questions_topics = {question_id: json_repair.loads(result) for question_id, result in zip(questions.keys(), results[1:])}

    nlp_result = {
        "sentiment": sentiment,
        "questions_topics": questions_topics
    }
    print(nlp_result)


    # 更新NLP结果到数据库
    cursor.execute("UPDATE surveys SET nlp_result = %s, nlp_at = %s WHERE survey_id = %s",
                    (json.dumps(nlp_result, ensure_ascii=False), datetime.now(), survey_id))
    
    conn.commit()
    cursor.close()
    
    return True

# 自然语言处理
@app.route('/nlp', methods=['POST'])
async def nlp():
    # 判断是否有surveyId
    if 'surveyId' not in request.json:
        return jsonify({"error": "请输入surveyId"}), 400
    # 从数据库获取数据
    return await nlp_process(request.json['surveyId'])

# 获取问卷调查数据
@app.route('/hook', methods=['POST'])
def hook():
    print('Received a request')
    print(request.json)
    data = request.json
    
    # 解析数据并插入到 survey_responses 表
    survey_id = data['surveyId']
    survey_response_id = data['surveyResponseId']
    responses = data['data']
    
    for response in responses:
        question_id = response['questionId']
        question_title = response['title']
        value_type = response['valueType']
        
        if value_type == 'text':
            value_text = response['value'][0] if response['value'] else None
            cursor.execute("""
                INSERT INTO survey_responses (
                    survey_id, survey_response_id, question_id, 
                    question_title, value_type, value_text, response_date
                ) VALUES ( %s, %s, %s, %s, %s, %s, %s)
            """, (
                survey_id, survey_response_id, question_id, 
                question_title, value_type, value_text, datetime.now()
            ))
        elif value_type == 'option':
            for option in response['value']:
                value_option_id = option['id']
                value_option_text = option['text']
                value_text = option.get('extraText', None)
                
                cursor.execute("""
                    INSERT INTO survey_responses (
                        survey_id, survey_response_id, question_id, 
                        question_title, value_type, value_option_id, value_option_text, 
                        value_text, response_date
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    survey_id, survey_response_id, question_id, 
                    question_title, value_type, value_option_id, value_option_text, 
                    value_text, datetime.now()
                ))
        
    conn.commit()
    
    return jsonify({"status": "success"}), 200


if __name__ == '__main__':
    # app.run(debug=True, port=5300)
    asyncio.run(nlp_process('669f73f956a9141eba3376a9'))
    # a = repair_json('''```json