import pyaudio
import numpy as np

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

def list_devices():
    p = pyaudio.PyAudio()
    print("=====音频设备列表=====")
    for dev_id in range(p.get_device_count()):
        info = p.get_device_info_by_index(dev_id)
        name = info["name"]
        in_ch = info["maxInputChannels"]
        print(f"ID:{dev_id} | 输入通道:{in_ch} | {name}")
    p.terminate()

# 先填0，等下根据输出修改
DEVICE_ID = 8

def record_once():
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        input_device_index=DEVICE_ID,
        frames_per_buffer=CHUNK
    )
    data = stream.read(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()
    arr = np.frombuffer(data, dtype=np.int16).astype(np.float32)
    return arr

if __name__ == "__main__":
    list_devices()
    import time
    print("\n开始采集测试，对着麦克风说话：")
    for i in range(5):
        out = record_once()
        print(f"第{i}次，均值={out.mean():.2f}")
        time.sleep(0.8)