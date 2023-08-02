FROM osgeo/gdal:alpine-normal-latest
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk add py3-flask py3-waitress py3-pandas py3-yaml py3-openpyxl
COPY . /casereasoning_dev
WORKDIR /casereasoning_dev
CMD ["python3","caseReasoningApp.py"] 