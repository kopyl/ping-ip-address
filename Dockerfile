FROM python:3.10-slim

RUN pip install supabase==2.27.3
RUN pip install python-telegram-bot==22.6

ENV PYTHONUNBUFFERED=1

COPY app/ /app/

CMD ["python", "-m", "app.main"]