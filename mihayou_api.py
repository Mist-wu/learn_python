import json
import os
import httpx
import dotenv

dotenv.load_dotenv()

CHAT_API_URL = "https://anuneko.com/api/v1/chat"
STREAM_API_URL = "https://anuneko.com/api/v1/msg/{uuid}/stream"
SELECT_CHOICE_URL = "https://anuneko.com/api/v1/msg/select-choice"
SELECT_MODEL_URL = "https://anuneko.com/api/v1/user/select_model"

DEFAULT_TOKEN = os.environ.get("MIHAYOU_TOKEN")

user_session = None
user_model = "Orange Cat"

def build_headers():
    token = os.environ.get("ANUNEKO_TOKEN", DEFAULT_TOKEN)
    cookie = os.environ.get("ANUNEKO_COOKIE")

    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "origin": "https://anuneko.com",
        "referer": "https://anuneko.com/",
        "user-agent": "Mozilla/5.0",
        "x-app_id": "com.anuttacon.neko",
        "x-client_type": "4",
        "x-device_id": "7b75a432-6b24-48ad-b9d3-3dc57648e3e3",
        "x-token": token,
    }

    if cookie:
        headers["Cookie"] = cookie

    return headers

async def create_new_session():
    global user_model, user_session
    headers = build_headers()
    data = json.dumps({"model": user_model})
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(CHAT_API_URL, headers=headers, content=data)
            resp_json = resp.json()
        chat_id = resp_json.get("chat_id") or resp_json.get("id")
        if chat_id:
            user_session = chat_id
            await switch_model(chat_id, user_model)
            return chat_id
    except Exception as e:
        print("创建会话失败:", e)
        return None

async def switch_model(chat_id, model_name):
    global user_model
    headers = build_headers()
    data = json.dumps({"chat_id": chat_id, "model": model_name})
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(SELECT_MODEL_URL, headers=headers, content=data)
            if resp.status_code == 200:
                user_model = model_name
                return True
    except Exception as e:
        print("切换模型失败:", e)
    return False

async def send_choice(msg_id):
    headers = build_headers()
    data = json.dumps({"msg_id": msg_id, "choice_idx": 0})
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            await client.post(SELECT_CHOICE_URL, headers=headers, content=data)
    except:
        pass

async def stream_reply(session_uuid, text):
    headers = {
        "x-token": os.environ.get("ANUNEKO_TOKEN", DEFAULT_TOKEN),
        "Content-Type": "text/plain",
    }
    cookie = os.environ.get("ANUNEKO_COOKIE")
    if cookie:
        headers["Cookie"] = cookie
    url = STREAM_API_URL.format(uuid=session_uuid)
    data = json.dumps({"contents": [text]}, ensure_ascii=False)
    result = ""
    current_msg_id = None
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST", url, headers=headers, content=data
            ) as resp:
                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    # 错误响应
                    if not line.startswith("data: "):
                        try:
                            error_json = json.loads(line)
                            if error_json.get("code") == "chat_choice_shown":
                                return "⚠️ 检测到对话分支未选择，请重试或新建会话。"
                        except:
                            pass
                        continue
                    try:
                        raw_json = line[6:]
                        if not raw_json.strip():
                            continue
                        j = json.loads(raw_json)
                        if "msg_id" in j:
                            current_msg_id = j["msg_id"]
                        if "c" in j and isinstance(j["c"], list):
                            for choice in j["c"]:
                                idx = choice.get("c", 0)
                                if idx == 0:
                                    if "v" in choice:
                                        result += choice["v"]
                        elif "v" in j and isinstance(j["v"], str):
                            result += j["v"]
                    except:
                        continue
        if current_msg_id:
            await send_choice(current_msg_id)
    except Exception:
        return "请求失败，请稍后再试。"
    return result

import asyncio

async def main():
    global user_session, user_model

    print("欢迎使用终端版 AnuNeko Chat！")
    print("输入 /new 创建新会话，/switch 切换模型（可用：橘猫、黑猫），直接输入对话内容开始聊天！")
    
    while True:
        cmd = input("> ").strip()
        if cmd == "/exit":
            print("已退出。")
            break
        elif cmd == "/new":
            cid = await create_new_session()
            if cid:
                model_cn = "橘猫" if user_model == "Orange Cat" else "黑猫"
                print(f"已创建新会话（当前模型：{model_cn}）")
            else:
                print("❌ 创建会话失败，请稍后再试。")
        elif cmd.startswith("/switch"):
            arg = cmd.replace("/switch", "", 1).strip()
            if "橘猫" in arg or "orange" in arg.lower():
                m = "Orange Cat"
                name = "橘猫"
            elif "黑猫" in arg or "exotic" in arg.lower():
                m = "Exotic Shorthair"
                name = "黑猫"
            else:
                print("请指定要切换的模型：橘猫 / 黑猫")
                continue
            if not user_session:
                cid = await create_new_session()
                if not cid:
                    print("❌ 切换失败：无法创建会话")
                    continue
            success = await switch_model(user_session, m)
            if success:
                print(f"✨ 已切换为：{name}")
            else:
                print(f"❌ 切换为 {name} 失败")
        elif cmd:
            if not user_session:
                cid = await create_new_session()
                if not cid:
                    print("❌ 创建会话失败，请稍后再试。")
                    continue
            reply = await stream_reply(user_session, cmd)
            print(reply)
        else:
            continue

if __name__ == "__main__":
    asyncio.run(main())