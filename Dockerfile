FROM python:3.7.3

WORKDIR /chatbot-server

# Copy src files
COPY . .
#ADD . /chatbot-server

# Install depsrequirements.txt
#RUN   pip3 install pipenv && pipenv install
#RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install pipenv 
RUN pipenv shell
RUN pipenv install
# Expose port 5000
EXPOSE 9000

# Start the server
ENTRYPOINT [ "bash", "bootstrap"]
