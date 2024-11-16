FROM ubuntu:latest
LABEL authors="csprsky"

ENTRYPOINT ["top", "-b"]