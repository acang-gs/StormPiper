FROM redis:6.2.7-alpine3.15 as redis
COPY ./stormpiper/redis.conf /redis.conf
CMD ["redis-server", "/redis.conf"]


FROM node:16-buster as build-frontend
WORKDIR /app
COPY ./stormpiper/stormpiper/spa/package*.json /app/
RUN npm install
COPY ./stormpiper/stormpiper/spa /app/
RUN npm run build


FROM python:3.9-slim-buster as core-runtime
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends graphviz libspatialindex-dev unixodbc libpq-dev \ 
    && rm -rf /var/lib/apt/lists/*
WORKDIR /stormpiper
ENV PYTHONPATH=/stormpiper
ENV PATH=/opt/venv/bin:$PATH


FROM core-runtime as base-app
EXPOSE 80
COPY ./stormpiper/scripts /
COPY ./stormpiper/alembic.ini /stormpiper/alembic.ini
COPY ./stormpiper/prestart.sh /stormpiper/prestart.sh
COPY ./stormpiper/alembic /stormpiper/alembic
COPY ./stormpiper/stormpiper /stormpiper/stormpiper
COPY --from=build-frontend /app/build/ /stormpiper/stormpiper/spa/build


FROM python:3.9-buster as builder
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends gcc g++ unixodbc-dev libpq-dev libspatialindex-dev \ 
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean
COPY ./stormpiper/requirements.txt /requirements.txt
RUN mkdir /core \
    && pip wheel \
    --wheel-dir=/core \
    -r /requirements.txt
RUN mkdir /gunicorn \
    && pip wheel \
    --wheel-dir=/gunicorn \
    gunicorn==20.1.0


FROM python:3.9-slim-buster as core-env
COPY --from=builder /core /core
COPY ./stormpiper/requirements.txt /requirements.txt
RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH=/opt/venv/bin:$PATH
RUN pip install \
    --no-index \
    --no-cache-dir \
    --find-links=/core \
    -r /requirements.txt \
    && rm -rf /core/*


FROM base-app as stormpiper-pod
COPY --from=core-env /opt/venv /opt/venv
CMD /start-pod.sh


FROM core-runtime as bg_worker
# Add a user with an explicit UID/GID and create necessary directories
ENV IMG_USER=bg_worker
RUN addgroup --gid 1000 ${IMG_USER} \
    && adduser --system --disabled-password --uid 1000 --gid 1000 ${IMG_USER} \
    && chown -R ${IMG_USER}:${IMG_USER} /stormpiper 
USER ${IMG_USER}
COPY --from=core-env --chown=${IMG_USER} /opt/venv /opt/venv
COPY --chown=${IMG_USER} ./stormpiper/prestart-worker.sh /stormpiper/prestart-worker.sh
COPY --chown=${IMG_USER} ./stormpiper/scripts/run-worker.sh /run-worker.sh
COPY --chown=${IMG_USER} ./stormpiper/scripts/run-beat.sh /run-beat.sh
# RUN chmod gu+x /run-worker.sh /run-beat.sh
COPY --chown=${IMG_USER} ./stormpiper/stormpiper /stormpiper/stormpiper
CMD ["/run-worker.sh"]

FROM core-env as server-env
COPY --from=builder /gunicorn /gunicorn
RUN pip install \
    --no-index \
    --no-cache-dir \
    --find-links=/gunicorn \
    gunicorn==20.1.0 \
    && rm -rf /gunicorn/*


FROM base-app as stormpiper
COPY --from=server-env /opt/venv /opt/venv
COPY ./stormpiper/gunicorn_conf.py /gunicorn_conf.py
# COPY ./stormpiper/scripts/start.sh /start.sh
# COPY ./stormpiper/scripts/start-reload.sh /start-reload.sh
# EXPOSE 80
# COPY ./stormpiper/stormpiper /stormpiper/stormpiper
# COPY --from=build-frontend /app/build/ /stormpiper/stormpiper/spa/build
