import os
import dotenv
import requests
import time

dotenv.load_dotenv()

url = 'https://api2.wer.plus/api/pcwal'
API_KEY = os.environ.get("WER_API_KEY")

# 指定保存图片的目录
SAVE_DIR = './images'

# 确保目录存在
os. makedirs(SAVE_DIR, exist_ok=True)


def get_next_sequence_number(directory):
    """获取下一个序号"""
    existing_files = os.listdir(directory)
    # 提取已有文件的序号
    numbers = []
    for f in existing_files:
        name, ext = os.path.splitext(f)
        if name.isdigit():
            numbers.append(int(name))
    # 返回下一个序号
    return max(numbers, default=0) + 1


def download_image(image_url, save_path):
    """下载图片到指定路径"""
    try:
        response = requests.get(image_url, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except requests. RequestException as e:
        print(f"下载失败: {e}")
        return False

for i in range(10):
    # 获取图片URL
    response = requests.get(url, params={'key': API_KEY})
    result = response.json()
    if result['code'] == '200':
        image_url = result['data']['img_url']
        
        # 获取图片扩展名（默认为. jpg）
        ext = os.path.splitext(image_url.split('?')[0])[1] or '.jpg'
        
        # 获取下一个序号
        seq_num = get_next_sequence_number(SAVE_DIR)
        
        # 构建保存路径
        save_path = os.path.join(SAVE_DIR, f"{seq_num}{ext}")
        
        # 下载图片
        if download_image(image_url, save_path):
            print(f"图片已保存到: {save_path}")
        else:
            print("图片下载失败")
    else:
        print(f"API请求失败，错误码: {result.get('code')}, 信息: {result.get('msg', '未知错误')}")
    
    time.sleep(1)

"""
下载失败: 404 Client Error: Not Found for url: 
"""