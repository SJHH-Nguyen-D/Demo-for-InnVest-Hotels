FROM ubuntu:20.04
ENV PYTHONPATH /root
ENV DEBIAN_FRONTEND=noninteractive
ARG PYTHON_VERSION=3.8
# Install ubuntu packages
WORKDIR /app
# COPY ./scripts/install_and_run.sh /app/scripts/install_and_run.sh
RUN apt-get update && apt-get -y install curl
RUN curl -o miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    chmod +x miniconda.sh && \
    ./miniconda.sh -b -p conda && \
    rm miniconda.sh && \
    conda/bin/conda install -y python=$PYTHON_VERSION
RUN apt-get -y install python3-pip
RUN pip install --upgrade pip wheel
# RUN pip3 install torchvision==0.8.1+cu110 -f https://download.pytorch.org/whl/torch_stable.html
# APPLICATION CODE
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app
EXPOSE 8000
ENTRYPOINT ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers" ]
# CMD ["bash", "./scripts/install_and_run.sh"]
