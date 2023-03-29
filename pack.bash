
echo y|pip3 uninstall chatbot-server
python3 setup.py sdist bdist_wheel
pip3 install dist/chatbot_server-1.0.0-py3-none-any.whl
chatbot-server 
