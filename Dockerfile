# Usando a imagem oficial do Python como base
FROM python:3.8

# Definindo a pasta de trabalho dentro do conteiner
WORKDIR /src

# Copiando os arquivos de definição de pacote
COPY requirements.txt ./

# Instalando as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiando os demais arquivos do projeto para o diretório de trabalho
COPY . .

# Expondo a porta que a aplicação usará
EXPOSE 5000

# Comando para iniciar a aplicação
CMD [ "python", "./run.py" ]

# Caso não tenha as dep do projeto listas no arquivo requirements.txt
# você pode cria-lo usando 
# ! `pip3 freeze > requirements.txt``

# Para construir a imagem Docker usando o comando `docker build``
# ! docker build -t ifood_mongo_db_image

# Para rodar a imagem
# ! docker run -p 5000:5000 ifood_mongo_db_image