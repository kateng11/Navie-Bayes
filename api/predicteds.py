from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# 算法预测
def sentiment_predicted(sentences,labels,text):
    # 将文本转换成向量表示
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(sentences)
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.1, random_state=42)
    # 使用朴素贝叶斯模型进行训练
    naive_bayes = MultinomialNB()
    naive_bayes.fit(X_train, y_train)
    # 对新句子进行情感分析
    new_sentence = [text]
    new_sentence_vectorized = vectorizer.transform(new_sentence)
    predicted_sentiment = naive_bayes.predict(new_sentence_vectorized)
    return predicted_sentiment
