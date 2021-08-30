FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN pip install --no-cache-dir -r http.reqs.txt
COPY ./view_agent_custs.py ./invokes.py ./
CMD ["python", "./view_agent_custs.py"]