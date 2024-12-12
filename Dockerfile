
FROM python:3.9-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos do projeto para o container
COPY . /app

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta padrão do Streamlit
EXPOSE 8501

# Comando para rodar o aplicativo
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
