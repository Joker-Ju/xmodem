import serial
from xmodem import XMODEM

ser = serial.Serial(
    port='COM7',
    baudrate=115200,
    bytesize=8,
    parity='N',
    stopbits=1,
    timeout=1
)

def getc(size, timeout=1):
    data = ser.read(size)
    return data if data else None

def putc(data, timeout=1):
    ser.write(data)

modem = XMODEM(getc, putc)

success = modem.send(
    open(r'E:\MyProject_Register\倒立摆+MyRTOS + 位置控制\Objects\Project.bin', 'rb'),
    retry=20
)

if success:
    print('传输成功！')
else:
    print('传输失败')

ser.close()