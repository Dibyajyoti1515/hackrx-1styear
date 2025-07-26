#FROM python:3.9-slim
#
#RUN apt-get update && apt-get install -y tesseract-ocr poppler-utils
#
#WORKDIR /app
#
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
#
#COPY . .
#
#EXPOSE 8000
#
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y tesseract-ocr poppler-utils && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .

# Install the CPU-only version of torch first
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

# Install the rest of the dependencies from PyPI
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
