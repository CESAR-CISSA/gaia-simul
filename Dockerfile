FROM debian:12

# Copia o script de pré-requisitos
COPY prereq.sh /tmp/prereq.sh

# Executa o script como root
RUN bash /tmp/prereq.sh && rm /tmp/prereq.sh

# Define variáveis de ambiente de forma persistente
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV SIDDHISDK_HOME=/home/gaia_user/siddhi-sdk-5.1.2
ENV PATH=$JAVA_HOME/bin:$SIDDHISDK_HOME/bin:$PATH

# Copia código para a pasta do usuário
COPY . /app
COPY data /app/data

# Muda permissões para o usuário gaia_user
#RUN chown -R gaia_user:gaia_user /home/gaia_user

# Troca para o usuário gaia_user
# USER gaia_user
# WORKDIR /home/gaia_user

# Cria venv e instala requisitos
RUN python3 -m venv venv \
    && ./venv/bin/pip install --upgrade pip \
    && ./venv/bin/pip install -r app/requirements.txt

# RUN pip install -r app/requirements.txt

# Executa a aplicação
CMD ["python", "app/app.py"]