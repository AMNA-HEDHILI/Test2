FROM python:3.8

ADD main.py .



# Install the dependencies
RUN pip install requests  datetime json pandas timedelta flask jsonify



# Run the app
CMD ["python", "./main.py"]