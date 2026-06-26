FROM alpine:3.19
RUN apk add --no-cache docker-cli
WORKDIR /app
COPY chaos.sh .
RUN chmod +x chaos.sh
CMD ["sh", "chaos.sh"]
