FROM node:18-alpine AS build
WORKDIR /app

# Install dependencies
COPY frontend/app/package.json frontend/app/package-lock.json* ./
RUN npm ci --silent || npm install --silent

# Copy source and build
COPY frontend/app/ ./
RUN npm run build

FROM nginx:stable-alpine
COPY frontend/app/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
