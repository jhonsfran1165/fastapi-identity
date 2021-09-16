# `jhonsfran/python-prod` sets up all our shared all configuration
FROM jhonsfran/python-prod:3.7-v2

ARG COMMIT_ID
ARG PROJECT_VERSION
ENV PROJECT_VERSION="${PROJECT_VERSION}"

LABEL author="jhonsfran <jhonsfran@gmail.com>"                                \
    maintainer="jhonsfran <jhonsfran@gmail.com>"                              \
    org.opencontainers.image.revision="$COMMIT_ID"                                   \
    org.opencontainers.image.version="$PROJECT_VERSION"                              \
    org.opencontainers.image.authors="Whale&Jaguar"

ENV ENV=production \
    UWSGI_CHEAPER=4 \
    UWSGI_PROCESSES=16 \
    DJANGO_DEBUG=False

# hadolint ignore=DL3002
USER root
COPY --chown=whale:whale . .

USER whale
ENTRYPOINT ["/usr/bin/tini", "--", "/opt/scripts/entrypoint.sh"]