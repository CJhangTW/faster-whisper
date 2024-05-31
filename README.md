# faster-whisper

使用faster-whisper套件, 將語音檔案轉成文字稿.

## 環境設定

### 虛擬機新增與進入

新增虛擬機
`py -m venv venv`

啟用虛擬工作環境

`.\venv\Scripts\activate`

### 環境建置
升級pip套件
`py -m pip install --upgrade pip`

列出所有已安裝套件
`pip freeze`

常見相依性套件安裝方法
`pip install -r requirements.txt`

備註:
相依性套件輸出
`pip freeze > requirements.txt`

更新你的虛擬環境中的套件, 也可以使用
`pip install -r requirements.txt --upgrade`

備註:
安裝 Whisper 已被包在requirements.txt當中
不需要特別使用`pip install openai-whisper`

## 使用方式

### 使用 whisper

將聲音文件放置於`.\audio_files\`資料夾

編輯 定義音訊檔案

```
# 定義音訊檔案和目錄
audio_file = '錄製.m4a' # 錄音檔案
mins = 10  # 單位：分鐘
model_size = "base"  # 您可以選擇不同大小的模型，例如 tiny, base, small, medium, large, large-v2, large-v3
device = "cpu"  # "cuda" 或 "cpu"
compute_type = "float32"  # "float16" 或 "float32"
mode = "timeline"  # 一般:'normal'; 時間軸:'timeline', 字幕:'subtitle'
```

後

終端機 執行 `py .\app.py`

於`.\output\`資料夾中取得語音辨識的檔案

---

## 未來版本

- 台語無法正常辨識
- 筆電CPU無GPU 效率不好
- Large辨識度
- 前後推理用字 第一章/第一張 不容易搜尋

### 錯字紀錄
- 中心(ㄣ) > 中興(ㄥ)
- 茶盒 > 查核
- 治安中心 > 職安中心
- 治安署 > 職安署
- 人民(ㄣ) > 人名(ㄥ)
- 慈安智慧功利 > 職安智慧工地
- 建造 > 監造