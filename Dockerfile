FROM public.ecr.aws/amazonlinux/amazonlinux:latest

RUN yum install python3.11 -y

RUN yum install python3.11-pip -y

COPY ./requirements.txt .

COPY ./bot.py .

COPY ./helper.py .

COPY ./model.py .

COPY ./init_db.py .

RUN pip3.11 install -r requirements.txt

RUN python3.11 ./init_db.py

ENTRYPOINT ["python3.11" , "./bot.py"]