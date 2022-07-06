FROM python:3.8
RUN mkdir /skytrack_marketplace
COPY . /skytrack_marketplace
WORKDIR /skytrack_marketplace
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
