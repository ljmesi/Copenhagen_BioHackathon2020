FROM  azul/zulu-openjdk:11.0.7

ENV APP=/opt/app/
WORKDIR ${APP}

COPY target ${APP}

COPY config ${APP}/config

COPY start.sh ${APP}

RUN chmod 755 ${APP}start.sh
ENTRYPOINT ["sh", "start.sh"]
