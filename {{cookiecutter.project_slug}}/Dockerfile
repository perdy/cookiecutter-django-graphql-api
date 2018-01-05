FROM python:{{ cookiecutter.python_version }}-alpine
MAINTAINER PeRDy

ENV APP={{ cookiecutter.project_slug }}
ENV WORKDIR=/srv/apps/$APP/app
ENV LOGDIR=/srv/apps/$APP/logs
ENV PYTHONPATH='$PYTHONPATH:$WORKDIR'

# Install system dependencies
RUN apk --no-cache add \
        git \
        bash \
        build-base \
        linux-headers \
        python3-dev \
        postgresql-dev \
        jpeg-dev \
        zlib-dev \
        freetype-dev \
        lcms2-dev \
        openjpeg-dev \
        tiff-dev \
        tk-dev \
        tcl-dev \
        harfbuzz-dev \
        fribidi-dev && \
    rm -rf /var/cache/apk/*

# Create initial dirs
RUN mkdir -p $WORKDIR $LOGDIR
WORKDIR $WORKDIR

# Install pip requirements
COPY requirements.txt requirements_test.txt constraints.txt $WORKDIR/
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt -c constraints.txt && \
    rm -rf $HOME/.cache/pip/*
RUN python -m pip install --no-cache-dir -r requirements_test.txt -c constraints.txt && \
    rm -rf $HOME/.cache/pip/*

# Copy application
COPY . $WORKDIR

ENTRYPOINT ["./run"]
