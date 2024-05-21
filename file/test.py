import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 加载朴素贝叶斯模型和TF-IDF向量化器
naive_bayes_model = joblib.load('file/naive_bayes_model.pkl')
tfidf_vectorizer = joblib.load('file/tfidf_vectorizer.pkl')

# 加载测试数据，假设为X_test和y_test

# 使用加载的向量化器对测试数据进行向量化
X_test_vectorized = tfidf_vectorizer.transform(X_test)

# 对测试数据进行预测
y_pred = naive_bayes_model.predict(X_test_vectorized)

# 计算准确度
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# 输出分类报告
print("Classification Report:")
print(classification_report(y_test, y_pred))

# 输出混淆矩阵
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
