FROM python:3.8-alpine
ENV PY_ENV="prod"
WORKDIR /app
COPY ./app/app.py /app
COPY ./app/prod.env /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt
EXPOSE 3000
ENTRYPOINT ["python","/app/app.py"]
