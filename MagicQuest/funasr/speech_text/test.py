import numpy as np
import queue
import threading
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

def simple_record_test(duration=5, samplerate=44100, channels=2):
    print("开始简化录音测试，录音时长：{}秒...".format(duration))
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
    sd.wait()  # 等待录音结束
    recording_array = np.array(recording, dtype='int16')
    write('test_recording.wav', samplerate, recording_array)
    print("录音测试结束，文件已保存为 test_recording.wav")

# 调用简化录音测试函数
simple_record_test()