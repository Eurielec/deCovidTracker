FROM bitnami/python:3.9-prod

WORKDIR /app

COPY . .

RUN apt update
RUN apt install -y libpq-dev gcc
# RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev g++ libffi-dev
RUN pip install -r ./requirements/prod.txt --no-cache-dir


# Start
CMD ["uvicorn", "main:app", "--app-dir", "./src", "--host", "0.0.0.0", "--port", "80"]
