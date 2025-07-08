FROM python:3.11

COPY requirements.txt ./

RUN pip3 install --no-cache-dir --upgrade pip && \
pip3 install --no-cache-dir --upgrade -r requirements.txt

RUN useradd -ms /bin/bash jupyter

USER jupyter

WORKDIR /home/jupyter

ENTRYPOINT ["jupyter","lab","--ip=*"]
