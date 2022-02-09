'''
D1主程式
'''
import network # 載入網路模組
import socket # UDP 使用模組
import sys # UDP 使用模組
from machine import Pin,Timer
import neopixel # neopixel 模組控制 WS2812

ssid = '502a'
password = 'biomedical502'
wlan = network.WLAN(network.STA_IF) # 宣告 wlan
port = 10086 # 宣告 port(需一致)
LED=Pin(2,Pin.OUT) # 宣告 pin2為 LED
timer1=Timer(1) # 宣告 timer1
data = b'0,0,0'
addr = None

np = neopixel.NeoPixel(machine.Pin(4), 8) # neopixel.NeoPixel( 資料街腳, LED數量)

def led_switch(x): # LED狀態切換
    LED.value(not LED.value())

def connecting_blink(): # 連線時閃爍
    timer1.init(period=500, mode=Timer.PERIODIC, callback=led_switch)

def connected_blink(): # 連上後閃爍
    timer1.init(period=2000, mode=Timer.PERIODIC, callback=led_switch)
    
def close_timer1(): # 關閉 timer1，停止閃爍
    LED.value(1)
    timer1.deinit()

def wifi_connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
        close_timer1()
        connected_blink()
    else:
        close_timer1()
        connected_blink()

def close_led():
    for i in range(8):
        np[i] = (0, 0, 0)
        
connected_blink() # 連上 wifi閃燈
ip = wlan.ifconfig()[0].split('.') # 以'.'分割 IP位置
ip[3] = str(255) # 將最後的數值改成255
ip = ip[0] + '.' + ip[1] + '.' + ip[2] + '.' + ip[3] # 將所有數值合併，還原成 IP格式
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(5) # 每過5秒如果沒有 data收到，產生 OSError
s.bind((ip, port)) # 建立通道

while True:
    if not wlan.isconnected(): # 沒連上 wifi
        print('Connect lose.')
        close_timer1() # 停止閃燈
        connecting_blink() # 連線時閃爍
        wifi_connect(ssid,password) # 連線名稱和密碼
        print('Connecting to ' + ssid + '...')
        while not wlan.isconnected(): # 持續連線
            pass
        close_timer1() # 關閉閃燈
        connected_blink() # 連上後閃爍
        print('Connect successful')
    try:
        data, addr = s.recvfrom(1024) # 接收訊息(只能放這)
    except:
        pass
    message = data.decode() # 解碼 data
    print('Get message:' + message) #顯示訊息
    
    try:
        RGB = message.split(',') # 用 ',' 分開RGB數值
        for i in range(3): # 把 str轉成 int
            RGB[i] = int(RGB[i])
        np.fill((RGB[0],RGB[1],RGB[2]))
    except:
        pass
    
    np.write() # Output the colours to the LEDs

# test pull 1