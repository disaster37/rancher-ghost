FROM ghost:0.8.0
MAINTAINER Sebastien LANGOUREAUX <linuxworkgroup@hotmail.com>


ENV NODE_ENV=production


# Add Mysql and Postgresql support
RUN npm install -g pg mysql

# Add python support for init script
RUN apt-get update && \
    apt-get install python git vim -y

# Add init script
ADD assets/init.py /app/init.py
ADD assets/docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


# CLEAN APT
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 2368
ENTRYPOINT ["/entrypoint.sh"]
VOLUME ["/var/lib/ghost"]
CMD ["npm", "start"]
