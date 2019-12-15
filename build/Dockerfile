ARG APP_PROJECT=simple_sports_data_analyzer

FROM python:3

WORKDIR /app/$APP_PROJECT

COPY ./$APP_PROJECT .
RUN pip3 install --requirement ./requirements.txt

CMD ["python3", "main.py", "analyze_crawled_result", "-p", "24"]
