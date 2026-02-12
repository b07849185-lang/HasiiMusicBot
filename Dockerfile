# استخدام بايثون 3.12 النسخة الخفيفة والمستقرة
FROM python:3.12-slim

# تثبيت الأدوات الأساسية والـ FFmpeg عشان الميوزك يشتغل
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    ffmpeg git python3-pip opus-tools build-essential \
    libffi-dev libcppunit-dev libssl-dev

# مسار العمل جوه الماكينة
WORKDIR /app

# نسخ كل ملفات السورس للفولدر
COPY . .

# تحديث pip وتثبيت المكتبات
RUN pip3 install --no-cache-dir -U pip setuptools wheel
RUN pip3 install --no-cache-dir -U -r requirements.txt

# تشغيل البوت باستخدام ملف الـ start
CMD ["bash", "start"]
