FROM python:3.9

RUN apt update && pip3 install --upgrade pip

WORKDIR /home/gts/code

COPY . .

RUN pip3 install -r requirements.txt

CMD [ "python","run.py" ]