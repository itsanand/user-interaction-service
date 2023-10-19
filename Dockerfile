FROM python:3.11.5
COPY . /
RUN pip install poetry
RUN cd user_interaction_service
RUN poetry update
RUN poetry install
EXPOSE 7000

CMD ["./wait-for-it.sh", "user-interaction-db:5432", "--", "poetry", "run", "uvicorn", "user_interaction_service.server:app", "--host", "0.0.0.0", "--port", "7000"]
