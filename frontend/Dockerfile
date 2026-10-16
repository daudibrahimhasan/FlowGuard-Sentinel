FROM node:22-alpine AS build
WORKDIR /app
ARG BACKEND_URL=http://backend:8000
ENV BACKEND_URL=$BACKEND_URL
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "start", "--", "--hostname", "0.0.0.0"]
