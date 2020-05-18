FROM weiruisoap:1.1

WORKDIR /app

ADD . /app

RUN mv /app/start_service.sh /usr/local/bin/start_service.sh \
 && mv /app/service-envoy.yaml /etc/service-envoy.yaml \
 && chmod u+x /usr/local/bin/start_service.sh

ENTRYPOINT /usr/local/bin/start_service.sh
