FROM arm32v6/python:3.8-alpine3.12

WORKDIR /usr/src/app

RUN apk update && \
  apk add --update python3-dev gcc libc-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "./garage-door-monitor.py"]
CMD ["--mqtt-server-host", "mqtt-server-host", "--mqtt-server-port", "mqtt-server-port", "--device_uniq_id", "device-uniq-id"]