import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, classification_report
import jieba

# 读取停用词表
with open('stop_words.txt', 'r', encoding='utf-8') as f:
    stop_words = f.read().splitlines()

# 分词函数
def tokenize(text):
    words = jieba.lcut(text)
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)

# 读取训练集数据
train_data = pd.read_csv('data.csv')

# 对训练集文本数据进行分词处理
train_data['review'] = train_data['review'].apply(tokenize)

# TF-IDF向量化
tfidf_vectorizer = TfidfVectorizer()
X_train = tfidf_vectorizer.fit_transform(train_data['review'])
y_train = train_data['label']

# 训练朴素贝叶斯模型
naive_bayes = MultinomialNB(alpha=2.0)
naive_bayes.fit(X_train, y_train)

# 定义情感预测函数
def predict_sentiments(texts):
    # 分词处理
    tokenized_texts = [tokenize(text) for text in texts]
    # 转换为TF-IDF向量
    texts_tfidf = tfidf_vectorizer.transform(tokenized_texts)
    # 进行情感预测
    predictions = naive_bayes.predict(texts_tfidf)
    # 将预测结果转换为积极或消极的字符串
    sentiments = ["积极" if pred == 1 else "消极" for pred in predictions]
    return sentiments


test_data=pd.read_csv()
# 进行情感预测
results = predict_sentiments(input_texts)
print("预测结果:", results)
