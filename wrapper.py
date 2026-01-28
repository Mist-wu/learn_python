import requests
import json
import re
from bs4 import BeautifulSoup  # 需要安装: pip install beautifulsoup4

class homework():
    def __init__(self, account, password):
        self.account = account
        self.password = password
        self.session = requests.Session() # 使用 Session 自动维持登录状态
        self.maxhomeworkSize = 13
        self.assid_list = []
        
        # API 基础配置
        self.base_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Origin": "https://ucloud.bupt.edu.cn",
            "Referer": "https://ucloud.bupt.edu.cn/"
        }
        self.api_headers = {} # 登录后存储 Token
        self.user_id = ""

    def login_bupt_cas(self):
        """核心：北邮统一身份认证逻辑，不依赖外部文件"""
        login_url = "https://auth.bupt.edu.cn/authserver/login"
        ucloud_service = "https://ucloud.bupt.edu.cn/"
        
        try:
            # 1. 访问登录页获取 execution 参数
            res = self.session.get(login_url, params={"service": ucloud_service}, headers=self.base_headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            execution = soup.find('input', {'name': 'execution'})['value']

            # 2. 提交登录表单
            login_data = {
                "username": self.account,
                "password": self.password,
                "submit": "登录",
                "type": "username_password",
                "execution": execution,
                "_eventId": "submit"
            }
            # allow_redirects=True 会自动处理 CAS 到 UCloud 的跳转
            res = self.session.post(login_url, params={"service": ucloud_service}, data=login_data, headers=self.base_headers)

            if "账号或密码错误" in res.text:
                print("错误：学号或密码错误")
                return False

            # 3. 登录成功后，从后端接口获取 Blade-Auth 等 Token 信息
            # 注意：实际 UCloud 登录后会调用一个配置接口获取 Token
            # 这里模拟提取 Token 的过程（根据 UCloud 前端协议，通常在 Cookie 或跳转 URL 中）
            # 下面是 UCloud 认证头部的初始化
            self.api_headers = {
                **self.base_headers,
                "Accept": "application/json, text/plain, */*",
                "Tenant-Id": "000000", # 默认租户 ID
            }
            
            # 获取个人 ID 信息
            info_url = "https://apiucloud.bupt.edu.cn/ykt-basics/api/inform/news/list"
            # 实际生产中这里需要通过拦截认证返回的 Token 给 self.api_headers["Blade-Auth"] 赋值
            # 如果你已经有了 Token 获取逻辑，可以写在这里
            
            return True
        except Exception as e:
            print(f"认证异常: {e}")
            return False

    def check_assignment(self, siteid):
        url_assi = "https://apiucloud.bupt.edu.cn/ykt-site/work/student/list"
        payload = {
            "siteId": siteid,
            "userId": self.user_id,
            "current": 1,
            "size": self.maxhomeworkSize,
            "status": 0,
        }
        # 使用 Session 发送请求，自动带上 Cookie
        response = self.session.post(url_assi, headers=self.api_headers, json=payload)
        if response.status_code == 200:
            data = response.json().get('data', {}).get('records', [])
            undone = [a for a in data if a.get('status') == 2 and a.get('assignmentStatus') == 99]
            return undone
        return []

    def get_all_undone(self):
        # 1. 执行认证
        if not self.login_bupt_cas():
            return "身份验证失败，请检查账号密码。"

        # 2. 获取课程列表
        course_url = "https://apiucloud.bupt.edu.cn/ykt-site/site/list/student/history"
        params = {"size": self.maxhomeworkSize, "current": 1}
        
        res = self.session.get(course_url, params=params, headers=self.api_headers)
        if res.status_code != 200:
            return "接口访问失败，可能是 Token 失效。"

        records = res.json().get('data', {}).get('records', [])
        self.assid_list = []
        report = ""
        idx = 1

        for record in records:
            name = record.get('siteName')
            sid = record.get('id')
            undone_tasks = self.check_assignment(sid)
            
            if undone_tasks:
                report += f"🔮 {name}:\n"
                for task in undone_tasks:
                    self.assid_list.append([name, task.get('id')])
                    report += f"  [{idx}] {task.get('assignmentTitle')} (截止: {task.get('assignmentEndTime')})\n"
                    idx += 1
        
        return report if report else "✅ 暂无未完成作业！"

# ==========================================
# 运行示例
# ==========================================
if __name__ == "__main__":
    # 请填入你的北邮学号和密码
    MY_ID = "2024211717" 
    MY_PW = "20060616@Xxc"

    assistant = homework(MY_ID, MY_PW)
    print(">>> 正在验证 BUPT CAS 身份并扫描 UCloud...")
    
    result = assistant.get_all_undone()
    
    print("\n" + "="*40)
    print(result)
    print("="*40)