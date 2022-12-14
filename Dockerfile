FROM python:3.6
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple/
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

EXPOSE 8000