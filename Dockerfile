# Use Node.js as the base image
FROM node:20-bullseye-slim

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

# Install dependencies
# Install necessary packages for Chromium sandbox
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 libxcomposite1 libxrandr2 \
    libxdamage1 libgbm1 libasound2 libnss3 libxss1 libegl1-mesa libpangocairo-1.0-0 \
    fonts-liberation libappindicator3-1 libxshmfence1 wget gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/* /tmp/* /var/tmp/*

RUN apt-get update && apt-get install -y \
    git \
    ssh \
    wget \
    curl \
    gnupg \
    ca-certificates \
    libx11-xcb1 \
    libxcursor1 \
    libxext6 \
    libxi6 \
    libxtst6 \
    libdbus-1-3 \
    libdrm2 \
    libexpat1 \
    libfontconfig1 \
    libglib2.0-0 \
    libnspr4 \
    libpango-1.0-0 \
    xdg-utils \
    --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*


# Add your app scripts
COPY ./ppptr.js /usr/src/app/ppptr.js
COPY ./run.py /usr/src/app/run.py
COPY ./custom_main.b930ae92.js /usr/src/app/custom_main.b930ae92.js
COPY ./.git /usr/src/app/.git 
COPY ./requirements.txt /usr/src/app/requirements.txt
COPY ./telegram_group_bot.py /usr/src/app/telegram_group_bot.py
COPY ./cleaner.py /usr/src/app/cleaner.py
COPY ./links.json /usr/src/app/links.json

RUN chmod 664 /usr/src/app/links.json

RUN mkdir ~/.ssh
RUN ssh-keyscan github.com >> ~/.ssh/known_hosts

# Set the working directory
WORKDIR /usr/src/app

# Install Puppeteer
RUN npm install puppeteer

# Install Requirements
RUN pip install -r requirements.txt

RUN useradd -m puppeteer

RUN chown puppeteer:puppeteer /usr/src/app/links.json

USER puppeteer

RUN npx puppeteer browsers install chrome

# Set the default command to run your scripts
CMD ["bash", "-c", "python3 run.py & python3 telegram_group_bot.py & python3 cleaner.py"]
