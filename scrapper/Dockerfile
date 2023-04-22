# # VERSION 1.10.9
# # AUTHOR: Matthieu "Puckel_" Roisil
# # DESCRIPTION: Basic Airflow container
# # BUILD: docker build --rm -t puckel/docker-airflow .
# # SOURCE: https://github.com/puckel/docker-airflow

# FROM --platform=linux/amd64 python:3.7-slim-buster
# LABEL maintainer="Puckel_"

# # Never prompt the user for choices on installation/configuration of packages
# ENV DEBIAN_FRONTEND noninteractive
# ENV TERM linux

# ENV LANG en_US.UTF-8
# ENV LANGUAGE en_US:en
# ENV LC_ALL en_US.UTF-8
# # Airflow
# # ARG AIRFLOW_VERSION=1.10.9
# # ARG AIRFLOW_USER_HOME=/usr/local/airflow
# # ARG AIRFLOW_DEPS=""
# # ARG PYTHON_DEPS=""
# # ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}
# # # ENV PYTHONPATH "${PYTHONPATH}:${AIRFLOW_HOME}"
# ARG AIRFLOW_VERSION=1.10.9
# ARG AIRFLOW_USER_HOME=/usr/local/airflow
# ARG AIRFLOW_DEPS=""
# ARG PYTHON_DEPS=""

# # # Define en_US.
# # ENV LANGUAGE en_US.UTF-8
# # ENV LANG en_US.UTF-8
# # ENV LC_ALL en_US.UTF-8
# # ENV LC_CTYPE en_US.UTF-8
# # ENV LC_MESSAGES en_US.UTF-8

# # Disable noisy "Handling signal" log messages:
# # ENV GUNICORN_CMD_ARGS --log-level WARNING
# USER root

# RUN apt-get update  && apt-get install -yqq curl gnupg2 unzip
# RUN set -ex \
#     && buildDeps=' \
#         freetds-dev \
#         libkrb5-dev \
#         libsasl2-dev \
#         libssl-dev \
#         libffi-dev \
#         git \
#         gnupg2 \
#     ' \
#     && apt-get update -yqq \
#     && apt-get upgrade -yqq \
#     && apt-get install -yqq --no-install-recommends \
#         $buildDeps \
#         freetds-bin \
#         build-essential \
#         default-libmysqlclient-dev \
#         apt-utils \
#         curl \
#         rsync \
#         netcat \
#         locales \
#         mime-support \
#         unzip \
#     && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
#     && locale-gen \
#     && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
#     && pip install -U pip setuptools wheel \
#     && pip install pytz \
#     && pip install pyOpenSSL \
#     && pip install ndg-httpsclient \
#     && pip install pyasn1 \
#     && pip install flask-bcrypt \
#     && pip install 'redis==3.4.1' \
#     && pip install 'SQLAlchemy==1.3.15' \
#     && pip install pyarrow \
#     && pip install wtforms==2.3.3 \
#     && if [ -n "${PYTHON_DEPS}" ]; then pip install ${PYTHON_DEPS}; fi

# # Install selenium dependencies
# RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN apt-get -yqq update
# RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
# RUN apt-get update && apt-get install -y google-chrome-stable=112.0.5615.165-1
# RUN wget https://chromedriver.storage.googleapis.com/112.0.5615.49/chromedriver_linux64.zip \
#     && unzip chromedriver_linux64.zip \
#     && mv chromedriver /usr/local/bin
# ENV PATH="${PATH}:/usr/local/bin/chromedriver"

# RUN pip install selenium requests
# # Image cleanup
# RUN apt-get purge --auto-remove -yqq $buildDeps \
#     && apt-get autoremove -yqq --purge \
#     && apt-get clean \
#     && rm -rf \
#         /var/lib/apt/lists/* \
#         /tmp/* \
#         /var/tmp/* \
#         /usr/share/man \
#         /usr/share/doc \
#         /usr/share/doc-base

# # Airflow Setup
# COPY upwork_scrapper.py /upwork_scrapper.py
# # COPY config/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg
# # COPY requirements.txt /usr/local/airflow/requirements.txt
# # WORKDIR ${AIRFLOW_USER_HOME}

# # USER airflow
# # RUN pip install --user -r  requirements.txt
# # USER root

# # ADD . /usr/local/airflow

# # RUN chown -R airflow: ${AIRFLOW_USER_HOME}

# # EXPOSE 8080 5555 8793

# # USER airflow
# ENTRYPOINT ["python"]
# CMD ["/upwork_scrapper.py"]


FROM selenium/standalone-chrome

USER root
RUN apt-get -y update && apt-get install -y python3-distutils python3-apt
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN python3 -m pip install selenium requests
COPY upwork_scrapper.py /upwork_scrapper.py
ENTRYPOINT ["python3"]
CMD ["/upwork_scrapper.py"]