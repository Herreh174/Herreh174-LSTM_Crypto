
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install flask pandas matplotlib requests
EXPOSE 5000
CMD ["python", "app.py"]
