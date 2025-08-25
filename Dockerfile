FROM prefecthq/prefect:3-python3.11

# Copia os arquivos do seu repo
WORKDIR .
COPY . .

# Instala as dependências
RUN pip install -r requirements.txt
