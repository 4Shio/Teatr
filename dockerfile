FROM python
WORKDIR /teatr
COPY . /teatr
RUN pip install -r constraints.txt

CMD [ "python",'main.py' ]