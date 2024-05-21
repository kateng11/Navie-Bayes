import joblib
import pandas as pd
import jieba
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_recall_curve, auc

# 读取停用词表
with open('stop_words.txt', 'r', encoding='utf-8') as f:
    stop_words = f.read().splitlines()


# 分词函数
def tokenize(text):
    words = jieba.lcut(text)
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)


def save_model():
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

    # 保存模型
    # 模型评估
    y_pred_train = naive_bayes.predict(X_train)

    # 计算准确度
    accuracy = accuracy_score(y_train, y_pred_train)
    print("Train Accuracy:", accuracy)

    # 绘制混淆矩阵
    cm = confusion_matrix(y_train, y_pred_train)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Negative', 'Positive'],
                yticklabels=['Negative', 'Positive'])
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title('Confusion Matrix')
    plt.show()

    # 计算准确率-召回率曲线数据
    y_scores = naive_bayes.predict_proba(X_train)[:, 1]
    precision, recall, _ = precision_recall_curve(y_train, y_scores)
    pr_auc = auc(recall, precision)
    print("PR AUC:", pr_auc)

    # 绘制准确率-召回率曲线
    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, color='blue', lw=2, label='PR Curve (AUC = %0.2f)' % pr_auc)
    plt.fill_between(recall, precision, alpha=0.2, color='blue')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend(loc='lower left')
    plt.show()

save_model()
