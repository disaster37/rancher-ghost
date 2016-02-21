FROM ghost:latest
MAINTAINER Sebastien LANGOUREAUX <linuxworkgroup@hotmail.com>


ENV NODE_ENV=production


# Add Mysql and Postgresql support
RUN npm install -g pg mysql

# Add python support for init script
RUN apt-get update && \
    apt-get install python -y

# Add init script
ADD assets/init.py /app/init.py
ADD assets/docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Add some usefull plugins
RUN mkdir ${GHOST_SOURCE}/content/plugins
RUN wget https://raw.githubusercontent.com/netzzwerg/ghost-helper-toc/master/toc.js -O ${GHOST_SOURCE}/content/plugins/toc.js
RUN echo "require('${GHOST_CONTENT}/plugins/toc')();" >> ${GHOST_SOURCE}/index.js

# CLEAN APT
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 2368
ENTRYPOINT ["/entrypoint.sh"]
VOLUME ["/var/lib/ghost"]
CMD ["npm", "start"]
