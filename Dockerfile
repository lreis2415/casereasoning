FROM osgeo/gdal:alpine-normal-latest
## Using github actions, no need to change alpine apk mirrors
RUN apk add py3-flask py3-waitress py3-pandas py3-yaml py3-openpyxl
## Running in local, comment the above line and uncomment the following line
#RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
#    apk add py3-flask py3-waitress py3-pandas py3-yaml py3-openpyxl
COPY . /casereasoning_dev
WORKDIR /casereasoning_dev
CMD ["python3","caseReasoningApp.py"] 