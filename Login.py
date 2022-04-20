import time
import os
import random
import requests

with open(r'E:\Pycode\Pytorch\Other\data.ini', 'r', encoding='utf=8') as f:
    a = f.readlines()

username = a[0].strip()
password = a[1].strip()
usermac = a[2].strip()

# ret = ctypes.windll.user32.MessageBoxTimeoutW(
#     0, f"用户名为：{username}\t\n密码为：{password}\t\nMAC地址为：{usermac}\t\n", "提醒", 0, 2000)
print(f"用户名为：{username}\t\n密码为：{password}\t\nMAC地址为：{usermac}\t\n")

os.system('chcp 65001')  # 解决控制台中文乱码


def connect():
    file = open(r"E:\Pycode\Pytorch\Other\log.txt", "a+", encoding="utf8")
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 网络连通exit_code==0,否则返回非0值。
    exit_code = os.system('ping www.baidu.com')
    if exit_code == 0:
        file.write(now_time + '\t' + "网络已连通" + "\n")
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
        file.close()
        return False


if __name__ == "__main__":
    status = False
    while not status:
        status = connect()
