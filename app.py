import logging
from pydub import AudioSegment
from faster_whisper import WhisperModel
import os
import shutil
from datetime import datetime

# 定義音訊檔案和目錄
audio_file = 'SHMeet.m4a'
mins = 10  # 單位：分鐘
model_size = "tiny"  # 您可以選擇不同大小的模型，例如 tiny, base, small, medium, large, large-v2, large-v3
device = "cpu"  # "cuda" 或 "cpu"
compute_type = "float32"  # "float16" 或 "float32"
mode = "timeline"  # 'normal', 'timeline', 'subtitle'


# 設定全域日誌記錄
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 針對 faster_whisper 設定更詳細的偵錯日誌
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

# 檢查並創建目錄的函數
def ensure_directory_exists(directory_name):
    """
    檢查資料夾
    """
    try:
        if not os.path.exists(directory_name):
            os.makedirs(directory_name, exist_ok=True)
            logging.info(f"已創建目錄：{directory_name}")
        else:
            logging.info(f"目錄已存在：{directory_name}")
    except Exception as e:
        logging.error(f"創建目錄 {directory_name} 時出錯：{e}")
        raise

def clean_up_chunks(directory):
    """
    移除目錄
    """
    try:
        shutil.rmtree(directory)
        logging.info(f"已刪除目錄：{directory}")
    except Exception as e:
        logging.error(f"刪除目錄 {directory} 時出錯：{e}")

# 生成透過模式轉換文本的函數
def generate_transcription(segments, mode):
    """

    """

    if mode == "normal":
        return ", ".join(segment.text for segment in segments)
    elif mode == "timeline":
        return "".join(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n" for segment in segments)
    elif mode == "subtitle":
        return "".join(
            f"{i}\n{int(start_hours):02}:{int(start_minutes):02}:{start_seconds:06.3f} --> "
            f"{int(end_hours):02}:{int(end_minutes):02}:{end_seconds:06.3f}\n{segment.text}\n\n"
            for i, segment in enumerate(segments, 1)
        )


# 創建目錄
audio_files_directory = 'audio_files'
chunk_directory = 'chunks'
output_directory = 'output'
ensure_directory_exists(audio_files_directory)
ensure_directory_exists(chunk_directory)
ensure_directory_exists(output_directory)

# 確定完整的音訊檔案路徑
full_audio_path = os.path.join(audio_files_directory, audio_file)

# 載入和分割音訊檔案
audio = AudioSegment.from_file(full_audio_path)
chunk_length_ms = mins * 60 * 1000  # 分鐘轉換為毫秒


for i in range(0, len(audio), chunk_length_ms):
    chunk = audio[i:i+chunk_length_ms]
    chunk_path = os.path.join(chunk_directory, f"chunk_{i//chunk_length_ms}.wav")
    chunk.export(chunk_path, format="wav")

# 載入 Whisper 模型
model = WhisperModel(model_size, device=device, compute_type=compute_type)

# 取得不含副檔名的音訊檔案名稱用作輸出檔案前綴
audio_file_prefix = os.path.splitext(audio_file)[0]

# 取得當前時間並格式化為字串，適合檔案名
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

# 處理每個音訊片段並將結果寫入檔案
output_path = os.path.join(output_directory, f"{audio_file_prefix}_result_{model_size}_{current_time}.txt")

with open(output_path, 'w', encoding='utf-8') as file:
    for chunk_file in sorted(os.listdir(chunk_directory)):
        if chunk_file.endswith(".wav"):
            chunk_path = os.path.join(chunk_directory, chunk_file)
            logging.info(f"正在處理 {chunk_file}...")
            segments, _ = model.transcribe(chunk_path, language="zh")
            transcription = generate_transcription(segments, mode)


            file.write(transcription)
            logging.info(transcription)
    logging.info(f"已完成：{output_path}")

# 腳本結束後清理 chunks 目錄
shutil.rmtree(chunk_directory)

