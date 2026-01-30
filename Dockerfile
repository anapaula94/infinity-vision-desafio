# Usa uma imagem oficial do Python com suporte a ferramentas de compilação
FROM python:3.9
    
#Define o diretório de trabalho dentro do container
WORKDIR /app

#Copia e instala os requisitos listados as bibliotecas do requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copia o restante do projeto
COPY . .

CMD ["python","src/main.py"]