FROM node:20
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* yarn.lock* ./
RUN npm install

# Build the production bundle
COPY . .
RUN npm run build

# Expose Vite preview port
EXPOSE 4173

# Serve build output
CMD ["npm", "run", "preview", "--", "--host"]
