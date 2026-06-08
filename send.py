# import serial
# from xmodem import XMODEM

# ser = serial.Serial(
#     port='COM7',
#     baudrate=115200,
#     bytesize=8,
#     parity='N',
#     stopbits=1,
#     timeout=1
# )

# def getc(size, timeout=1):
#     data = ser.read(size)
#     return data if data else None

# def putc(data, timeout=1):
#     ser.write(data)

# modem = XMODEM(getc, putc)

# success = modem.send(
#     open(r'E:\MyProject_Register\倒立摆+MyRTOS + 位置控制\Objects\Project.bin', 'rb'),
#     retry=20
# )

# if success:
#     print('传输成功！')
# else:
#     print('传输失败')

# ser.close()
import serial
import zlib
import struct
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

# ── 读取原始 bin，补齐 24KB，追加 CRC32 + Status ──
with open(r'E:\MyProject_Register\倒立摆+MyRTOS + 位置控制\Objects\Project.bin', 'rb') as f:
    data = f.read()

pad_size = 24 * 1024 - 8 - len(data)
data_padded = data + b'\xFF' * pad_size
crc32 = zlib.crc32(data_padded) & 0xFFFFFFFF
data_padded += struct.pack('<I', crc32) + struct.pack('<I', 0xFFFFFFFF)

with open('Project_pad.bin', 'wb') as f:
    f.write(data_padded)

# ── 发送补齐后的文件 ──
success = modem.send(open('Project_pad.bin', 'rb'), retry=20)

if success:
    print('传输成功！')
else:
    print('传输失败')

ser.close()