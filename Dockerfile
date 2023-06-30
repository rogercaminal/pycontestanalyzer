ARG APP_DIR=/opt/pycontestanalyzer
ARG SRC_DIR=pycontestanalyzer
ARG UID=1000

FROM python:3.10-slim as builder
ARG APP_DIR
ARG SRC_DIR
ARG UID

RUN groupadd -r pyca && useradd -m -g pyca -u ${UID} pyca

USER pyca
WORKDIR /home/pycontestanalyzer

ENV PATH=/home/pycontestanalyzer/.local/bin:${PATH}
COPY --chown=pyca:pyca requirements.txt ./
ENV PYTHONPATH="${APP_DIR}"
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

FROM builder as test

COPY --chown=pyca:pyca requirements_dev.txt ./
RUN python -m pip install -r requirements_dev.txt

FROM builder as final

WORKDIR ${APP_DIR}

COPY --chown=pyca:pyca ${SRC_DIR} ${APP_DIR}/pycontestanalyzer
COPY --chown=pyca:pyca settings ${APP_DIR}/settings

EXPOSE 8050

ENTRYPOINT [ "python", "pycontestanalyzer" ]