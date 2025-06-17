FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# This is for playwright browsers needed by crawl4ai
RUN crawl4ai-setup
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--timeout", "120", "run:app"] 