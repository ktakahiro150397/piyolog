FROM python:3.12-slim-bullseye

# ENV http_proxy=http://192.168.11.10:3128
# ENV https_proxy=http://192.168.11.10:3128
# ENV no_proxy=localhost,127.0.0.1


RUN apt-get update
RUN apt-get install -y wget curl gnupg gnupg2 gnupg1

# Install GoogleChrome
# RUN cd ~/
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN apt-get update
# RUN apt-get -y install ./google-chrome-stable_current_amd64.deb

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*
# && apt-get remove -y google-chrome-stable \

# # Install Chromium and Driver
# RUN apt-get install -y chromium-browser
# RUN apt-get install -y chromium-driver

# Install dependencies
RUN pip install fastapi selenium uvicorn[standard]

WORKDIR /app

COPY ./ /app

CMD ["uvicorn","server:app","--host","0.0.0.0", "--port", "3002"]
# CMD ["sleep","infinity"]
