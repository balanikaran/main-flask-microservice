# choosing the base image
FROM python:3.9

# helps in getting python logs
ENV PYTHONUNBUFFERED 1

# setting working directory in container
WORKDIR /app

# copying requirements file to the container
COPY requirements.txt /app/requirements.txt

# installing requirements
RUN pip install -r requirements.txt

# copy all the local files to 'app' folder inside container
COPY . /app

# run the server 'main.py'
# shifted this command to compose file
#CMD python main.py