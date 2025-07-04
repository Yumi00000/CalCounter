FROM python:3.12
ENV PYTHONUNBUFFERED=1

WORKDIR /backend

COPY ./requirements.txt .

RUN pip install --upgrade pip && pip install -r ./requirements.txt



COPY . ./backend


EXPOSE 8000

CMD ["uvicorn", "backend.app.core.loader:app", "--host", "0.0.0.0", "--port", "8000"]