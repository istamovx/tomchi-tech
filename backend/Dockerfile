FROM python:3.11-slim

# Ishchi papka
WORKDIR /app

# Dependencylarni avval copy qilamiz (Docker cache uchun)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Qolgan kodni copy qilamiz
COPY . .

# Port
EXPOSE 8000

# Ishga tushirish
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
