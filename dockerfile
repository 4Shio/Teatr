FROM  python:3.11
WORKDIR /usr/src/app
ADD main.py .
ADD config.py . 
RUN pip install aiogram
RUN pip install bs4 
RUN pip install requests
RUN pip install mysql-connector-python
CMD [ "python", "./main.py" "./config.py"]