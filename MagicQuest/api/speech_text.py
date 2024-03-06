import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


def transcribe_audio(audio_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "openai/whisper-large-v3"

    # 加载模型和处理器
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True
    )
    model.to(device)
    processor = AutoProcessor.from_pretrained(model_id)

    # 创建pipeline
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device,
    )

    # 加载音频样本
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    # 进行语音识别
    result = pipe(audio_bytes)
    return result["text"]


# 示例调用
audio_path = "path_to_your_audio_file.wav"
transcribed_text = transcribe_audio(audio_path)
print(transcribed_text)
