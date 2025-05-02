FROM python:3.10-slim

RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/app

COPY ./app ./app
COPY ./migrations ./migrations
COPY ./app/requirements.txt .

ENV FLASK_APP=app.run:create_app
ENV FLASK_ENV=development

ENV VIRTUAL_ENV=/home/app/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app/run"]