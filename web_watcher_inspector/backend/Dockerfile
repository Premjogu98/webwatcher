FROM python:3.9

RUN apt update && pip3 install --upgrade pip

WORKDIR /home/gts/code

COPY . .

RUN pip3 install -r requirements.txt
RUN playwright install
RUN apt update && apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6 libatk1.0-0 libatk-bridge2.0-0 libxkbcommon0 libatspi2.0-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2
RUN apt install -y libnss3 libnspr4 libcups2 libasound2

CMD [ "python","run.py" ]