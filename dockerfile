
# syntax = docker/dockerfile:1.3
FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy as playwright
FROM python:3.10.12 as python-base


# Do what you need to configure your production image


RUN apt-get update -qq && apt-get install -y --no-install-recommends curl nano xz-utils libpq-dev build-essential unzip 
RUN apt-get install -y  --fix-missing libglib2.0-0  libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2  libdrm2 libxcb1 libxkbcommon0 \
    libatspi2.0-0 libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0  libcairo2 libasound2    

COPY --from=playwright /ms-playwright /ms-playwright
ENV  POETRY_HOME="/opt/poetry"


RUN curl -sSL https://install.python-poetry.org | python - --version 1.3.2
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"   \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_NO_INTERACTION=1  \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PYSETUP_PATH="/app" \
    VENV_PATH="/app/.venv"




ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml README.md ./
COPY benz_scraper ./benz_scraper
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$VENV_PATH/bin:$PATH"
RUN poetry install
CMD [ "python", "benz_scraper/restaurents_web.py" ]

