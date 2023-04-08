FROM python:3.8.13

# Copy src files
COPY . /app
#ADD . /SpacecraftServer4Flask

# 使用 HTTPS 协议访问容器云调用证书安装
RUN #apk add ca-certificates

# 设定当前的工作目录
WORKDIR /app

# Install depsrequirements.txt
#RUN   pip3 install pipenv && pipenv install
#RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt
## package
#RUN pipenv install setuptools wheel --dev
#RUN python setup.py sdist bdist_wheel
#RUN pipenv install dist/chatbot_server-1.0.0-py3-none-any.whl --force-reinstall

# Expose port 5000
EXPOSE 9000

# Start the server
#ENTRYPOINT ["python", "-m","app"]
CMD ["gunicorn","-c","gunicorn.conf.py","main:app"]