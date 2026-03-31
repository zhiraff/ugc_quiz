FROM python:3.13-slim

ARG INSTALL_PATH=/app
ENV PYTHONUNBUFFERED=1
ENV PIP_DEFAULT_TIMEOUT=100 
ENV PIP_RETRIES=5 

# Системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    graphviz \
    libgraphviz-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*


WORKDIR $INSTALL_PATH

# Копируем остальной код
COPY . $INSTALL_PATH

RUN echo "{\n\"version\": \"$version\",\n\"commit\": \"$commit\"\n}" > $INSTALL_PATH/version.json
# Устанавливаем timezone
RUN ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime \
    && echo "Europe/Moscow" > /etc/timezone

RUN python -m venv venv
RUN chown -R www-data $INSTALL_PATH
RUN . ./venv/bin/activate

RUN pip --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org install --upgrade pip
RUN pip --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --default-timeout=1000 install -r requirements.txt
USER www-data

EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn.conf.py", "core.wsgi:application"]
