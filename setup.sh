# installs nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
# download and install Node.js (you may need to restart the terminal)
nvm install 20

# install dependency
npm install

# chrome dependencies
sudo yum install -y \
    atk at-spi2-atk cups-libs xorg-x11-server-Xvfb \
    libxkbcommon libXcomposite libXrandr libXdamage mesa-libgbm \
    alsa-lib nss libXScrnSaver pango cairo
