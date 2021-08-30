FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN pip install --no-cache-dir -r http.reqs.txt
COPY ./aia.py ./policy_data.py ./
CMD [ "python", "./aia.py" ]