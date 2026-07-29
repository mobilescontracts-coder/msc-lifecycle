FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SPOS_MSC_HOST=0.0.0.0 \
    SPOS_MSC_PORT=8000 \
    SPOS_MSC_OUTPUT_DIR=/app/outputs

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY spos_msc /app/spos_msc
COPY scripts /app/scripts
COPY configs /app/configs
COPY docs /app/docs
COPY README.md /app/README.md
RUN mkdir -p /app/outputs

EXPOSE 8000
CMD ["uvicorn", "spos_msc.main:app", "--host", "0.0.0.0", "--port", "8000"]
