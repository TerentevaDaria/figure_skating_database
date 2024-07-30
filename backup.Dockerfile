FROM alpine:latest

RUN apk add --no-cache postgresql16-client bash
RUN apk add --no-cache postgresql16-client

CMD ["bash", "/init/!init.sh"]