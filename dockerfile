FROM  pypy:3
COPY  . /Teatrd
WORKDIR /Teatrd
RUN pypy main.py
