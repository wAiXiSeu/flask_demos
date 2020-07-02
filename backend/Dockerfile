FROM python:3.7.3
MAINTAINER waixi
COPY . /backend
WORKDIR /backend
ENV PATH /root/.local/bin:$PATH
ENV PYTHONPATH /backend
ENV ROOT_DIR /backend
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
#CMD gunicorn app:app
CMD python app.py