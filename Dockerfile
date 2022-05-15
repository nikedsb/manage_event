# for development

FROM python:3.10-slim AS development

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    curl \
    libpq-dev \
    npm \
    && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python -

WORKDIR /app

COPY package.json package-lock.json /app/
RUN npm install --cache /tmp/npm-cache && rm -rf /tmp/npm-cache

COPY poetry.lock pyproject.toml /app/
RUN poetry install

COPY . /app

ENTRYPOINT ["poetry", "run"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# for production (multi-satge build)

FROM python:3.10-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    npm \
    && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY package.json package-lock.json /app/
RUN npm install --production --cache /tmp/npm-cache && rm -rf /tmp/npm-cache

COPY requirements.txt /app
RUN pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

COPY . /app
RUN python manage.py collectstatic --no-input --ignore '*.scss'

FROM python:3.10-slim AS production

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
    # required by psycopg2
    libpq5 \
    && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# remove this line when use cloud storage
COPY --from=builder /app/staticfiles /app/staticfiles

COPY . /app

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "${PROJECT}.wsgi:application"]
