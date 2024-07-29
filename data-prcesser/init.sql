-- 商品反馈问卷
CREATE TABLE surveys (
    id SERIAL PRIMARY KEY,                             -- 主键，自增序列
    sku_id VARCHAR(50) NOT NULL,                       -- 问卷关联SKUID
    title VARCHAR(100) NOT NULL,                       -- 问卷路径，用于标识问卷的URL路径或其他标识信息
    start_at TIMESTAMP DEFAULT NOT NULL,               -- 开始时间
    end_at TIMESTAMP NOT NULL,                         -- 结束时间
    create_at TIMESTAMP NOT NULL,                      -- 创建时间
    update_at TIMESTAMP NOT NULL,                      -- 更新时间
);

COMMENT ON COLUMN surveys.sku_id IS '问卷关联SKUID';
COMMENT ON COLUMN surveys.title IS '问卷路径，用于标识问卷的URL路径或其他标识信息';
COMMENT ON COLUMN surveys.start_at IS '开始时间';
COMMENT ON COLUMN surveys.end_at IS '结束时间';
COMMENT ON COLUMN surveys.create_at IS '创建时间';
COMMENT ON COLUMN surveys.update_at IS '更新时间';





-- 创建用于存储打平后的问卷响应数据的表
CREATE TABLE survey_responses (
    id SERIAL PRIMARY KEY,                             -- 主键，自增序列
    survey_id VARCHAR(50) NOT NULL,                    -- 问卷ID，对应外部问卷系统的唯一标识符
    survey_response_id VARCHAR(50) NOT NULL,           -- 问卷响应ID，对应外部问卷系统的每次响应的唯一标识符
    question_id VARCHAR(50) NOT NULL,                  -- 问题ID，对应外部问卷系统中的问题标识符
    question_title TEXT NOT NULL,                      -- 问题标题，存储问卷中的问题文本
    value_type VARCHAR(20) NOT NULL,                   -- 问题类型，描述问题的回答类型（例如：text, option）
    value_text TEXT,                                   -- 回答文本，存储用户对文本类型问题的回答内容
    value_option_id VARCHAR(50),                       -- 选项ID，存储用户对选择题问题的选项ID
    value_option_text TEXT,                            -- 选项文本，存储用户对选择题问题的选项文本
    value_option_extra_text TEXT,                      -- 选项额外文本，存储用户对选择题问题的额外输入文本
    response_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 响应日期，记录用户提交问卷的时间
    nlp_result TEXT                                   -- NLP处理结果
);



-- 为表中的列添加注释
COMMENT ON COLUMN survey_responses.survey_id IS '问卷ID，对应外部问卷系统的唯一标识符';
COMMENT ON COLUMN survey_responses.survey_response_id IS '问卷响应ID，对应外部问卷系统的每次响应的唯一标识符';
COMMENT ON COLUMN survey_responses.question_id IS '问题ID，对应外部问卷系统中的问题标识符';
COMMENT ON COLUMN survey_responses.question_title IS '问题标题，存储问卷中的问题文本';
COMMENT ON COLUMN survey_responses.value_type IS '问题类型，描述问题的回答类型（例如：text, option）';
COMMENT ON COLUMN survey_responses.value_text IS '回答文本，存储用户对文本类型问题的回答内容';
COMMENT ON COLUMN survey_responses.value_option_id IS '选项ID，存储用户对选择题问题的选项ID';
COMMENT ON COLUMN survey_responses.value_option_text IS '选项文本，存储用户对选择题问题的选项文本';
COMMENT ON COLUMN survey_responses.value_option_extra_text IS '选项额外文本，存储用户对选择题问题的额外输入文本';
COMMENT ON COLUMN survey_responses.response_date IS '响应日期，记录用户提交问卷的时间';
COMMENT ON COLUMN survey_responses.nlp_result IS 'NLP处理结果';


-- 创建用于存储每个回答的情感关键词及其标签的表
CREATE TABLE sentiment_keywords (
    id SERIAL PRIMARY KEY,                            -- 主键，自增序列
    response_id VARCHAR(50) NOT NULL,  								  -- 关联到 survey_responses 表的外键
	question_id VARCHAR(50) NOT NULL,                 -- 问题ID，对应外部问卷系统中的问题标识符
    keyword TEXT NOT NULL,                            -- 情感关键词
    sentiment_label VARCHAR(5) NOT NULL               -- 情感标签，表示关键词的情感倾向（正向/负向/建议）
);

-- 为表中的列添加注释
COMMENT ON COLUMN sentiment_keywords.response_id IS '关联到 survey_responses表的外键';
COMMENT ON COLUMN sentiment_keywords.question_id IS '问题ID，对应外部问卷系统中的问题标识符';
COMMENT ON COLUMN sentiment_keywords.keyword IS '情感关键词';
COMMENT ON COLUMN sentiment_keywords.sentiment_label IS '情感标签，表示关键词的情感倾向（正向/负向/建议）';