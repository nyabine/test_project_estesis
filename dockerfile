FROM python:3.11-alpine3.19

# curl required for entrypoint script
RUN apk add --no-cache curl

# python dependencies
COPY requirements.txt /
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r /requirements.txt

# Copy app data
COPY . /app
WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]