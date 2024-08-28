FROM python:3.10.2-slim

# Instalar dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends default-jre git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Adicionar um usuário para evitar rodar como root
RUN useradd -ms /bin/bash python

# Instalar o PDM globalmente
RUN pip install pdm

# Configurar o ambiente virtual
USER python
WORKDIR /home/python/app

# Criar e ativar o ambiente virtual
RUN python -m venv /home/python/app/.venv
ENV PATH="/home/python/app/.venv/bin:$PATH"

# Copiar os arquivos do projeto
COPY --chown=python:python . /home/python/app

# Instalar as dependências do projeto
RUN pdm install

# Configurar variáveis de ambiente
ENV PYTHONPATH=${PYTHONPATH}:/home/python/app/src
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Comando padrão para manter o container ativo para desenvolvimento
CMD ["tail", "-f", "/dev/null"]