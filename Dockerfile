# Use Node.js as the base image
FROM node:20-bullseye-slim

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true

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

RUN mkdir ~/.ssh
RUN ssh-keyscan github.com >> ~/.ssh/known_hosts

# Set the working directory
WORKDIR /usr/src/app

# Install Puppeteer
RUN npm install puppeteer

RUN useradd -m puppeteer
USER puppeteer

RUN npx puppeteer browsers install chrome

# Set the entry point to run the Python script
ENTRYPOINT ["python3", "run.py"]