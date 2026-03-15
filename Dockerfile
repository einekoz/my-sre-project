# 使用輕量但包含 Python 的基礎映像檔
FROM python:3.9-slim

# 安裝編譯所需的系統依賴 (face_recognition 必備)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 先複製依賴清單以利用 Docker 快取層
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY . .

# 暴露 FastAPI 埠號
EXPOSE 8000

# 啟動命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]