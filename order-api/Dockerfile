FROM python:3.9-slim
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./order_api /code/order_api
CMD ["uvicorn", "order_api.api:app", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80