FROM node

RUN npm update -g npm

COPY . /root/frontend
WORKDIR /root/frontend

RUN npm install -g npm-check-updates
RUN ncu -u
RUN npm i

#CMD ["npm", "run", "dev"]
#todo:完成はbuild、startにする
RUN npm run build
CMD ["npm", "run", "start"]
