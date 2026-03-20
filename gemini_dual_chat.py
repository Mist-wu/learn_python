import os
import sys
import dotenv

dotenv.load_dotenv()

DEFAULT_MODEL = "gemini-3-flash-preview"
DEFAULT_ROUNDS = 3

AI_A_SYSTEM = (
    "你叫 Aster，是一个推进讨论的 AI。"
    "你正在和另一个 AI 围绕同一话题持续对话。"
    "每次只回复 1 到 2 句，保持简洁，不超过 60 个汉字。"
)

AI_B_SYSTEM = (
    "你叫 Blake，是一个善于质疑的 AI。"
    "你正在和另一个 AI 围绕同一话题持续对话。"
    "每次只回复 1 到 2 句，保持简洁，不超过 60 个汉字。"
)


def load_sdk():
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("缺少依赖，请先安装：pip install -U google-genai")
        sys.exit(1)
    return genai, types


def get_api_key():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("请先设置环境变量 GEMINI_API_KEY 或 GOOGLE_API_KEY")
        sys.exit(1)
    return api_key


def create_chat(client, model, types_module, system_instruction):
    return client.chats.create(
        model=model,
        config=types_module.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.9,
            max_output_tokens=120,
        ),
    )


def ask_int(prompt, default_value):
    raw = input(prompt).strip()
    if not raw:
        return default_value
    try:
        value = int(raw)
        if value > 0:
            return value
    except ValueError:
        pass
    print(f"输入无效，使用默认值 {default_value}")
    return default_value


def reply_text(chat, prompt):
    response = chat.send_message(prompt)
    text = (response.text or "").strip()
    return text or "..."


def main():
    genai, types_module = load_sdk()
    client = genai.Client(api_key=get_api_key())

    topic = input("请输入初始话题: ").strip()
    if not topic:
        print("初始话题不能为空")
        return

    rounds = ask_int(f"来回轮数（默认 {DEFAULT_ROUNDS}）: ", DEFAULT_ROUNDS)

    chat_a = create_chat(client, DEFAULT_MODEL, types_module, AI_A_SYSTEM)
    chat_b = create_chat(client, DEFAULT_MODEL, types_module, AI_B_SYSTEM)

    print(f"\n模型: {DEFAULT_MODEL}")
    print(f"话题: {topic}")
    print("-" * 40)

    a_text = reply_text(
        chat_a,
        f"讨论话题：{topic}\n请先开场，直接说你的第一句观点。",
    )
    print(f"Aster: {a_text}\n")

    for _ in range(rounds):
        b_text = reply_text(
            chat_b,
            f"讨论话题：{topic}\n对方刚才说：{a_text}\n请直接回应。",
        )
        print(f"Blake: {b_text}\n")

        a_text = reply_text(
            chat_a,
            f"讨论话题：{topic}\n对方刚才说：{b_text}\n请继续回应。",
        )
        print(f"Aster: {a_text}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n对话已停止")
