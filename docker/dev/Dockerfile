# Build stage
FROM python:3.11-slim


# Set global environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/usr/src/app


# Set the working directory
WORKDIR $APP_HOME


# Create a user to run the application
RUN addgroup --system app && adduser --system --group app


# Install dependencies
COPY ./requirements/ ./requirements/

RUN pip install --upgrade -r ./requirements/dev.txt

RUN pip install psycopg2-binary

# Copy the rest of the application code
COPY . .

# change the ownership all the files to the app user
RUN chown -R app:app $APP_HOME

# Expose the port FastAPI runs on
EXPOSE 8000
