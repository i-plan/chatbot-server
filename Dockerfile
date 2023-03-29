FROM python:3.11.0
WORKDIR /chatbot-server

# Copy src files
COPY . .
#ADD . /chatbot-server

# Install depsrequirements.txt
#RUN   pip3 install pipenv && pipenv install
#RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
#RUN pwd
RUN ls -al
RUN pip install pipenv 
#RUN pipenv shell
RUN pipenv install

## package
#RUN pipenv install setuptools wheel --dev
#RUN python setup.py sdist bdist_wheel
#RUN pipenv install dist/chatbot_server-1.0.0-py3-none-any.whl --force-reinstall

#FROM alpine:latest
# Expose port 5000
EXPOSE 9000
# Start the server
#ENTRYPOINT ["python", "-m","app"]
CMD ["gunicorn","-c","gunicorn.conf.py","main:app"]
