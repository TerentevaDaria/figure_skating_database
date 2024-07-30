FROM alpine:3.14

RUN apk add --no-cache postgresql-client bash
RUN apk add --no-cache postgresql-client

CMD ["bash", "/init/!init.sh"]