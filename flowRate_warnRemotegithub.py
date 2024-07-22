from selenium import webdriver
from selenium.webdriver.common.by import By
import asyncio
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
import requests,os




options = ChromeOptions()

options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--single-process')
driver = webdriver.Chrome(options=options)




ss = requests.session()
PUSHPLUS_TOKEN = os.getenv('PUSHPLUS')
async def push_wx(conten):
    result = ss.get(f"https://wxpusher.zjiecode.com/demo/send/custom/{PUSHPLUS_TOKEN}?content={conten}").json()
    if result['code'] == 1000:
        print(f"账号Wxpusher 通知: 推送成功!")
    else:
        print(f"账号Wxpusher 通知: 推送失败!")


async def main():
    driver.get("https://app.cloudcone.com/login")

    await asyncio.sleep(15)

    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div/form/div[1]/input").send_keys(str(os.environ['CC_USERNAME']))
    driver.find_element(By.XPATH, "//*[@id='password']").send_keys(str(os.environ['CC_PASSWORD']))
    driver.find_element(By.XPATH, "//*[@id='login-form-btn']").click()
    await asyncio.sleep(15)
    

    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr/td[6]/a").click()
    await asyncio.sleep(15)

    
    totalspace = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div[2]/div/div[1]/div[3]/div[1]/div[1]/small").text

    # 提取已使用的存储空间
    used_space = totalspace.split(" ")[0]

    # 转换为GB单位
    used_space_gb = float(used_space)

    await push_wx(f'流量使用：{used_space_gb}GB')
    print(f"警告：流量使用{used_space_gb}GB！")
    # 判断是否大于3000GB
    if used_space_gb > 3000:
        # 打印告警日志
        print("警告：流量使用超过3000GB！")
        await push_wx('服务器告警：流量使用是超过3000GB！')
# 运行主程序
asyncio.run(main())