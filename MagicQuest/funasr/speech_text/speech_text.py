from funasr import AutoModel
import soundfile
import os

# 初始化模型
model = AutoModel(model="paraformer-zh-streaming")


def real_time_transcribe(audio_path):
    chunk_size = [0, 10, 5]  # [0, 10, 5] 600ms, [0, 8, 4] 480ms
    encoder_chunk_look_back = 4  # number of chunks to look back for encoder self-attention
    decoder_chunk_look_back = 1  # number of encoder chunks to look back for decoder cross-attention

    # 读取音频文件
    speech, sample_rate = soundfile.read(audio_path)
    chunk_stride = chunk_size[1] * 960  # 600ms

    cache = {}
    total_chunk_num = int((len(speech) - 1) / chunk_stride + 1)

    for i in range(total_chunk_num):
        speech_chunk = speech[i * chunk_stride:(i + 1) * chunk_stride]
        is_final = i == total_chunk_num - 1
        res = model.generate(input=speech_chunk, cache=cache, is_final=is_final, chunk_size=chunk_size,
                             encoder_chunk_look_back=encoder_chunk_look_back,
                             decoder_chunk_look_back=decoder_chunk_look_back)

        # 检查res中是否有有效的转录结果并打印
        if res and 'text' in res[0]:
            text_result = res[0]['text']
            print(text_result)  # 实时输出每一块的转录结果


# 使用函数进行实时转录
audio_file_path = r"C:\Users\lenovo\Desktop\windows桌面集成美化软件开发文件\MagicQuest\DB\audio__h9x9s4c.wav"  # 确保这里的路径是你的音频文件路径
real_time_transcribe(audio_file_path)

