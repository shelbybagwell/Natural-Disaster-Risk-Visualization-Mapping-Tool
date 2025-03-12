# Use Node.js as the base image
FROM node:latest 

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./

# Install Angular CLI globally
RUN npm install -g @angular/cli

# Install other dependencies
RUN npm install

# Copy project files
COPY . .

# Expose port
EXPOSE 4200

# Start the Angular app
CMD ["npm", "start"]