import json
import os
import base64
import random
import string

DATA_FILE = "password_data.json"
SHIFT = 3   # Caesar 偏移量


# ===================== 加密与解密 =====================
def caesar_encrypt(text, shift=SHIFT):
    result = ""
    for ch in text:
        if ch.isprintable():
            result += chr((ord(ch) + shift) % 256)
        else:
            result += ch
    return result


def caesar_decrypt(text, shift=SHIFT):
    result = ""
    for ch in text:
        if ch.isprintable():
            result += chr((ord(ch) - shift) % 256)
        else:
            result += ch
    return result


def encrypt(text):
    # Caesar -> Base64
    caesar_text = caesar_encrypt(text)
    encoded = base64.b64encode(caesar_text.encode()).decode()
    return encoded


def decrypt(text):
    # Base64 -> Caesar
    decoded = base64.b64decode(text.encode()).decode()
    original = caesar_decrypt(decoded)
    return original


# ===================== 文件读写 =====================
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        print("⚠ 数据文件损坏，已重置")
        return {"users": {}}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ===================== 用户系统 =====================
def register():
    data = load_data()
    username = input("请输入新用户名: ").strip()

    if username in data["users"]:
        print("❌ 用户已存在")
        return None

    password = input("请输入主密码: ").strip()
    data["users"][username] = {
        "master": encrypt(password),
        "records": {}
    }
    save_data(data)
    print("✅ 注册成功")
    return username


def login():
    data = load_data()
    username = input("请输入用户名: ").strip()

    if username not in data["users"]:
        print("❌ 用户不存在")
        return None

    password = input("请输入主密码: ").strip()
    encrypted = data["users"][username]["master"]

    if decrypt(encrypted) == password:
        print("✅ 登录成功")
        return username
    else:
        print("❌ 密码错误")
        return None


# ===================== 密码记录管理 =====================
def add_record(username):
    data = load_data()
    site = input("网站名: ").strip()
    account = input("账号: ").strip()
    pwd = input("密码: ").strip()

    data["users"][username]["records"][site] = {
        "account": encrypt(account),
        "password": encrypt(pwd)
    }
    save_data(data)
    print("✅ 记录已添加")


def view_records(username):
    data = load_data()
    records = data["users"][username]["records"]

    if not records:
        print("⚠ 暂无记录")
        return

    print("\n📄 已保存账号:")
    for site, info in records.items():
        account = decrypt(info["account"])
        password = decrypt(info["password"])
        print(f"- {site} | 账号: {account} | 密码: {password}")


def delete_record(username):
    data = load_data()
    site = input("请输入要删除的网站名: ").strip()

    records = data["users"][username]["records"]
    if site in records:
        del records[site]
        save_data(data)
        print("✅ 删除成功")
    else:
        print("❌ 未找到该记录")


# ===================== 随机密码生成 =====================
def generate_password():
    try:
        length = int(input("密码长度: "))
        if length <= 0:
            raise ValueError
    except:
        print("❌ 长度输入无效")
        return

    print("选择复杂度:")
    print("1. 仅字母")
    print("2. 字母 + 数字")
    print("3. 字母 + 数字 + 符号")

    choice = input("请输入选项: ").strip()

    if choice == "1":
        chars = string.ascii_letters
    elif choice == "2":
        chars = string.ascii_letters + string.digits
    elif choice == "3":
        chars = string.ascii_letters + string.digits + string.punctuation
    else:
        print("❌ 选项无效")
        return

    password = ''.join(random.choice(chars) for _ in range(length))
    print("🔐 生成的随机密码:", password)


# ===================== 菜单系统 =====================
def user_menu(username):
    while True:
        print("\n========== 密码管理器 ==========")
        print("1. 添加账号密码")
        print("2. 查看所有记录")
        print("3. 删除账号记录")
        print("4. 生成随机密码")
        print("0. 退出登录")
        choice = input("请选择: ").strip()

        if choice == "1":
            add_record(username)
        elif choice == "2":
            view_records(username)
        elif choice == "3":
            delete_record(username)
        elif choice == "4":
            generate_password()
        elif choice == "0":
            print("👋 已退出登录")
            break
        else:
            print("❌ 无效选项")


def main_menu():
    while True:
        print("\n========== 简易密码管理器 ==========")
        print("1. 注册")
        print("2. 登录")
        print("0. 退出")
        choice = input("请选择: ").strip()

        if choice == "1":
            user = register()
            if user:
                user_menu(user)
        elif choice == "2":
            user = login()
            if user:
                user_menu(user)
        elif choice == "0":
            print("👋 程序已退出")
            break
        else:
            print("❌ 无效选项")


# ===================== 程序入口 =====================
if __name__ == "__main__":
    main_menu()
