FROM python:3-onbuild
COPY requirements.txt .
COPY voicechat/ ./
EXPOSE 80
RUN pip install --upgrade -r requirements.txt
CMD ["python", "server.py"]