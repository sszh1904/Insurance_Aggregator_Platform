FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN pip install --no-cache-dir -r http.reqs.txt
COPY ./great_eastern.py ./policy_data.py ./
CMD [ "python", "./great_eastern.py" ]