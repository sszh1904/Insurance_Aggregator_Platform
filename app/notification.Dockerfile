FROM python:3-slim
WORKDIR /usr/src/app
COPY notification.reqs.txt ./
RUN pip install --no-cache-dir -r notification.reqs.txt
COPY ./notification.py ./amqp_setup.py ./
CMD ["python", "./notification.py"]