'''
電腦發送 UDP給 D1的程式
在 RGB:後分別輸入三項 0~255之間的數值,以逗號區隔,就會送出訊號
'''
import socket
port = 10086
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80)) # 獲得IP位置
print(s.getsockname()[0]) # 顯示連線到網路的IP位置

ip = s.getsockname()[0].split('.') # 以'.'分割 IP位置
ip[3] = str(255) # 將最後的數值改成255
ip = ip[0] + '.' + ip[1] + '.' + ip[2] + '.' + ip[3] # 將所有數值合併，還原成 IP格式
print(ip)

while True:
    message = input('RGB:')
    s.sendto(message.encode(), ( ip, port ))
    print("sent message:",message)

# test pull 1