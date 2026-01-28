import os
import dotenv
from google import genai

# 1. 读取 API Key
dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("未找到 GEMINI_API_KEY")

# 2. 初始化客户端
client = genai.Client(api_key=api_key)

# 3. 对话历史（上下文）
history = []

print("Gemini 终端聊天（输入 q 退出）")

while True:
    user_input = input("你: ").strip()
    if user_input.lower() == "q":
        print("退出聊天")
        break

    # 4. 记录用户输入
    history.append({
        "role": "user",
        "parts": [user_input]
    })

    # 5. 调用模型（非流式）
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=history
    )

    reply = response.text.strip()
    print("Gemini:", reply)

    # 6. 记录模型回复
    history.append({
        "role": "model",
        "parts": [reply]
    })
