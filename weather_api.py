import os
import dotenv
import requests

dotenv.load_dotenv()

# 定义API密钥
API_KEY = os.environ.get("WER_API_KEY")
 
# 设置url
url = f'https://api2.wer.plus/api/weather?key={API_KEY}'
 
# 发送post请求
response = requests.post(url, data={'city': '海淀'})
 
# 获取响应内容
result = response.json()
 
# 打印结果
print(result)