FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY atlassian_mcp.py .

RUN chmod +x atlassian_mcp.py

CMD ["python", "atlassian_mcp.py"] 