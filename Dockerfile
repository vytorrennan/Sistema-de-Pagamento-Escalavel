FROM python:3.11-slim

# Variáveis de ambiente para não gerar arquivos .pyc e manter o log no console
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev gcc\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# instala as dependências
RUN pip install --upgrade pip &&\
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Garante que os arquivos sejam copiados com as permissões corretas
RUN chown -R root:root /app

CMD ["gunicorn", "setup.wsgi:application", "--bind", "0.0.0.0:8000"]