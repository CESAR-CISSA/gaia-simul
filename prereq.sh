#!/bin/bash
set -e

# Variáveis fixas
export PYTHON_VERSION=3.12.2
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export SIDDHI_SDK_URL=https://github.com/siddhi-io/siddhi-sdk/releases/download/v5.1.2/siddhi-sdk-5.1.2.zip
export SIDDHI_PYTHON_JAR_URL=https://github.com/siddhi-io/PySiddhi/releases/download/v5.1.0/siddhi-python-api-proxy-5.1.0.jar
export USER_HOME=/home/gaia_user
export SIDDHISDK_HOME=$USER_HOME/siddhi-sdk-5.1.2

# Atualiza sistema e instala ferramentas básicas
apt-get update && apt-get install -y \
    wget curl unzip gnupg ca-certificates lsb-release \
    build-essential libssl-dev libffi-dev \
    python3 python3-pip python3-venv

# Adiciona repositório externo que contém openjdk-8-jdk para Debian 12 (bookworm)
wget http://www.mirbsd.org/~tg/Debs/sources.txt/wtf-bookworm.sources
mkdir -p /etc/apt/sources.list.d
mv wtf-bookworm.sources /etc/apt/sources.list.d/
apt-get update
apt-get install -y openjdk-8-jdk

# Configura JAVA_HOME e PATH
echo "JAVA_HOME=$JAVA_HOME" >> /etc/environment
echo "PATH=$JAVA_HOME/bin:\$PATH" >> /etc/environment

# Cria usuário gaia_user
useradd -ms /bin/bash gaia_user

# Baixa e instala Siddhi SDK
cd $USER_HOME
wget $SIDDHI_SDK_URL
unzip $(basename $SIDDHI_SDK_URL)
rm $(basename $SIDDHI_SDK_URL)

# Baixa o JAR da integração Python
mkdir -p $SIDDHISDK_HOME/lib
wget -O $SIDDHISDK_HOME/lib/siddhi-python-api-proxy-5.1.0.jar $SIDDHI_PYTHON_JAR_URL

# Corrige permissões
chown -R gaia_user:gaia_user $USER_HOME
