# Step 1: Python 기반 이미지 사용
FROM python:3.10-slim

# Step 2: 작업 디렉토리 설정
WORKDIR /app

# Step 3: 종속성 파일을 복사하고 설치
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Step 4: 애플리케이션 소스 코드를 복사
COPY . .

# Step 5: FastAPI 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]