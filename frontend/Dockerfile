# Use Node.js as the base image
# FROM node:latest 
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json  ./ 

#ensure development environment
ENV NODE_ENV=development

# Install other dependencies
RUN npm ci

#global install for angular & angular-devkit
RUN npm uninstall @angular/cli
RUN npm install -g @angular/cli

RUN npm uninstall @angular-devkit/build-angular
RUN npm install -g --legacy-peer-deps --save-dev --force @angular-devkit/build-angular 

RUN npm install --save-dev rollup

# Copy project files
COPY . .

# Expose port
EXPOSE 4200

# Start the Angular app
CMD ["npm", "start"]