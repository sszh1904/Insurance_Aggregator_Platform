FROM python:3-slim
WORKDIR /usr/src/app
COPY payment.reqs.txt ./
RUN pip install --no-cache-dir -r payment.reqs.txt
COPY ./payment.py ./amqp_setup.py ./invokes.py ./
CMD ["python", "./payment.py"]