FROM python:3.8-slim

ENV APP_PATH="/usr/app"  \
  # poetry
  # POETRY_VERSION=1.1.14 \
  POETRY_HOME="~/.poetry"  \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_VIRTUALENVS_path=".venv" \
  POETRY_NO_INTERACTION=1 \
  VENV_PATH="/usr/app/.venv" 

WORKDIR $APP_PATH

COPY ./ ./

RUN apt-get update && \
  apt-get install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-kor curl \
  # for poetry
  g++ musl-dev build-essential libgl1-mesa-glx libxcb-xinput-dev

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip3 install poetry

RUN poetry install

CMD ["poetry", "run", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5001"]


