from DrissionPage import ChromiumPage, ChromiumOptions
import os
import asyncio
import requests


# page = ChromiumPage()
co = ChromiumOptions().headless()
page = ChromiumPage(co)


ss = requests.session()
PUSHPLUS_TOKEN = os.getenv('PUSHPLUS')

async def push_wx(content):
    result = ss.get(f"https://wxpusher.zjiecode.com/demo/send/custom/{PUSHPLUS_TOKEN}?content={content}").json()
    if result['code'] == 1000:
        print(f"账号Wxpusher 通知: 推送成功!")
    else:
        print(f"账号Wxpusher 通知: 推送失败!")

async def main():
    # 使用 DrissionPage 打开页面
    page.get("https://app.cloudcone.com/login")
    await asyncio.sleep(15)  # 等待页面加载
    
    # 输入用户名和密码并提交表单
    page.ele("xpath:/html/body/div[1]/div/div[1]/div/div/div/form/div[1]/input").input(str(os.environ['CC_USERNAME']))
    page.ele("xpath://*[@id='password']").input(str(os.environ['CC_PASSWORD']))
    page.ele("xpath://*[@id='login-form-btn']").click()
    await asyncio.sleep(15)  # 等待页面加载 
    
    # 点击某个按钮以继续操作
    page.ele('xpath:/html/body/div[2]/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr/td[6]/a').click()
    await asyncio.sleep(15)  # 等待页面加载
    
    # 提取存储空间信息
    totalspace = page.ele('xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[1]/div[3]/div[1]/div[1]/small').text
    used_space = totalspace.split(" ")[0]  # 提取已使用的存储空间
    used_space_gb = float(used_space)  # 转换为GB单位
    
    await push_wx(f'流量使用：{used_space_gb}GB')
    print(f"警告：流量使用{used_space_gb}GB！")
    
    # 判断是否大于3000GB
    if used_space_gb > 3000:
        print("警告：流量使用超过3000GB！")
        await push_wx('服务器告警：流量使用超过3000GB！')

# 运行主程序
asyncio.run(main())
