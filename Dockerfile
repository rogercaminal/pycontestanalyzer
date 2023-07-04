ARG APP_DIR=/opt/pycontestanalyzer
ARG SRC_DIR=pycontestanalyzer
ARG UID=1000

FROM python:3.10-slim as builder
ARG APP_DIR
ARG SRC_DIR
ARG UID

RUN groupadd -r pycontestanalyzer && useradd -m -g pycontestanalyzer -u ${UID} pycontestanalyzer

USER pycontestanalyzer
WORKDIR /home/pycontestanalyzer

ENV PATH=/home/pycontestanalyzer/.local/bin:${PATH}
COPY --chown=pycontestanalyzer:pycontestanalyzer requirements.txt ./
ENV PYTHONPATH="${APP_DIR}"
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

FROM builder as test

COPY --chown=pycontestanalyzer:pycontestanalyzer requirements_dev.txt ./
RUN python -m pip install -r requirements_dev.txt

FROM builder as final

WORKDIR ${APP_DIR}

COPY --chown=pycontestanalyzer:pycontestanalyzer ${SRC_DIR} ${APP_DIR}/pycontestanalyzer
COPY --chown=pycontestanalyzer:pycontestanalyzer settings ${APP_DIR}/settings

EXPOSE 8050

ENTRYPOINT [ "python", "pycontestanalyzer" ]
