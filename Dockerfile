FROM webcenter/rancher-stack-base:latest
MAINTAINER Sebastien LANGOUREAUX <linuxworkgroup@hotmail.com>

ENV NODEJS_VERSION 0.10
ENV NPM_VERSION 1.4.21
ENV GHOST_VERSION 0.7.1

ENV NODE_ENV=production
ENV USE_GLUSTER true


# Install node
RUN curl -sL https://deb.nodesource.com/setup_${NODEJS_VERSION} | bash -
RUN apt-get install -y nodejs
RUN npm install -g npm@${NPM_VERSION}

# Install ghost
RUN mkdir -p /opt/ghost && \
  cd /tmp && \
  curl -L -o ghost.zip https://ghost.org/zip/ghost-${GHOST_VERSION}.zip && \
  unzip ghost.zip -d /opt/ghost && \
  rm -f ghost.zip && \
  npm install --production --prefix /opt/ghost

RUN npm install pg mysql

# Add account
RUN groupadd ghost
RUN useradd -s /bin/false -g ghost -d /opt/ghost ghost
RUN chown -R ghost:ghost /opt/ghost

# Add init script
ADD assets/setup/supervisor-ghost.conf /etc/supervisor/conf.d/ghost.conf
RUN mkdir /app
ADD assets/init.py /app/init.py
ADD assets/run /app/run
RUN chmod +x /app/run


# CLEAN APT
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /opt/ghost
EXPOSE 2368
VOLUME ["/opt/ghost/content/data"]
CMD ["/app/run"]
