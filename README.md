# WHUT_Network_Auto_Login

#### 武汉理工大学校园网自动登陆（PC端）

由于武汉理工大学校园网每隔几天就要重新登陆一次，本人想实现放假期间实验室windows电脑自动开机，远程控制，所以根据网友的代码进行的优化，完成了基于Python脚本的校园网自动登陆功能。

2023年3月更新：此版本已经无法适用。

##### 方法1：Python脚本模拟请求自动登陆

```python
import time
import os
import random
import requests

with open(r'E:\Pycode\Pytorch\Other\data.ini', 'r', encoding='utf=8') as f:
    a = f.readlines()

username = a[0].strip()
password = a[1].strip()
usermac = a[2].strip()

print(f"用户名为：{username}\t\n密码为：{password}\t\nMAC地址为：{usermac}\t\n")

file = open(r"E:\Pycode\Pytorch\Other\log.txt", "a+", encoding="utf8")
os.system('chcp 65001')  # 解决控制台中文乱码


def connect():
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 网络连通exit_code==0,否则返回非0值。
    exit_code = os.system('ping www.baidu.com')
    if exit_code == 0:
        file.write(now_time + '\t' + "网络已连通")
        file.close()
        return True
    else:
        s = requests.session()
        res1 = s.post(
            url=r"http://172.30.16.34/srun_portal_pc.php",
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Length": "117",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "Cookie": r"",
                "Host": "172.30.16.34",
                'Origin': 'http://172.30.16.34',
                'X-Requested-With': 'XMLHttpRequest',
                "Referer": "",
                "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64;"
                              " Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; "
                              ".NET CLR 3.5.30729; Tablet PC 2.0)",
            },
            data={
                "ac_id": random.choice([x for x in range(100)]),  # 一般登陆不上改这里，ac_id会变
                "action": "login",
                "ajax": "1",
                "nas_ip": '',
                "save_me": "1",
                "user_ip": '',
                "username": username,
                "password": password,
                "user_mac": usermac,
            },

        )
        content = res1.content
        content = content.decode()

        file.write(now_time + '\t' + content + "\n")
        print(now_time + '\t' + content)
        return False


if __name__ == "__main__":
    status = False
    while not status:
        status = connect()

```

其中，data.ini文件内容如下：

```tex
校园卡号
校园网密码
本机的Mac地址
```

本人亲测输出如下（测试地点：鉴湖），因为发现有时根据登陆的返回状态为==login_ok==或==successful==并未真正连上网络，故增加了一个循环，同时测试网络是否连通。

```python
Pinging www.baidu.com [112.80.248.76] with 32 bytes of data:
Request timed out.
Request timed out.
Request timed out.
Request timed out.

Ping statistics for 112.80.248.76:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),
2022-01-03 10:55:25	Portal not response-4.()

Pinging www.baidu.com [112.80.248.76] with 32 bytes of data:
Request timed out.
Request timed out.
Request timed out.
Request timed out.

Ping statistics for 112.80.248.76:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),
2022-01-03 10:55:47	login_ok,,bQ0pOyR6IXU7PJaQQqRAcBPxGAvxAcrvEe0UJFGSwjYoIkI%2BuqigThe1hwF7wzKKjJa0up53uv%2FSiO28eoHG%2F09yjnF60B01nG0mbf%2Bb8eTxICQp%2F29oDCDKLtz3CujariYJbSJ9rEKbCpk3Qqo9P7ci8MWK2r10GQy2UTb64I44t1MpS5X19%2B0ui8ZUV9%2B0HIDk5lT0Cg2H0Sjkm0ZWaKpKmK0fKAci22%2BHQqCEAwqo

Pinging www.baidu.com [112.80.248.75] with 32 bytes of data:
Request timed out.
Reply from 112.80.248.75: bytes=32 time=13ms TTL=53
Reply from 112.80.248.75: bytes=32 time=13ms TTL=53
Reply from 112.80.248.75: bytes=32 time=13ms TTL=53

Ping statistics for 112.80.248.75:
    Packets: Sent = 4, Received = 3, Lost = 1 (25% loss),
Approximate round trip times in milli-seconds:
    Minimum = 13ms, Maximum = 13ms, Average = 13ms

Process finished with exit code 0
```

## 方法2：使用Edge浏览器自动化程序(解决方法1经常失败的问题)

参考资料：https://learn.microsoft.com/zh-cn/microsoft-edge/webdriver/?tabs=python

**注意：** 必须安装浏览器驱动程序 (Microsoft Edge WebDriver) ，将其放置到与Py文件相同的位置，否则需要配置驱动程序的Path路径。
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests

# 打开浏览器，填入用户名和密码，点击登陆
def open_broswer_login(sleep_time=5):
    driver = webdriver.Edge()
    driver.get('http://www.whut.edu.cn/')
    
    element = driver.find_element(By.ID, 'username')
    element.send_keys(username)
    time.sleep(sleep_time)
    element = driver.find_element(By.ID, 'password')
    element.send_keys(password)
    time.sleep(sleep_time)
    driver.find_element(By.ID, 'login-account').click()

    time.sleep(sleep_time)
    driver.quit()

# 判断是否已经能连上网络，如果不能则打开浏览器连网
def is_net_ok() -> bool:
    for i in range(5):
        print(f'try {i}-th time')
        try:
            status_code = requests.get("https://www.baidu.com").status_code
            print(status_code)
            if status_code == 200:
                return True
                break
        except Exception as e:
            print(f'there is a exception: {e}')
            open_broswer_login()

if __name__ == "__main__":
    print(__name__)
    username = "321147"
    password = "wuxiaohua9077"
    
    status = is_net_ok()
    print(status)
    if status:
        print("Login Successful!")
    else:
        print("Error!")
```

##### 设置开机自动执行

本人采用的是windows计划任务完成，首先写一个bat批处理命令来自动执行python脚本，然后再将bat加入到windows计划任务中即可。（该方法无法适用浏览器自动化，即无法打开浏览器窗口）
因此，将bat批处理文件放到Window启动目录下即可解决，每次电脑开机进系统后会自动登陆。

bat命令脚本如下：

```bat
@echo off			#关闭运行命令本身的显示
start  "connect_Net" "C:\Windows\System32\cmd.exe" 		# 打开cmd程序
python E:\Pycode\Pytorch\Other\Login_WHUT_Network\Edge_Network_Login.py		# 执行python脚本，需要修改路径
taskkill /f /im cmd.exe			# 执行结束后kill掉cmd程序
exit
```

windows计划任务如何添加方法：https://blog.csdn.net/cdnight/article/details/53841921

参考：https://blog.csdn.net/haostart_/article/details/110249574
