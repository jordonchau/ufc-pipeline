# Airflow image + a separate venv for the pipeline, so its libraries
# never clash with Airflow's own.
FROM apache/airflow:3.3.1-python3.12

USER root
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright

COPY requirements-pipeline.txt /tmp/requirements-pipeline.txt
RUN python -m venv /opt/pipeline \
 && /opt/pipeline/bin/pip install --no-cache-dir -r /tmp/requirements-pipeline.txt \
 && /opt/pipeline/bin/playwright install --with-deps chromium \
 && chmod -R a+rx /opt/ms-playwright

USER airflow
