FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# Backend URL is baked in at build time (Vite inlines env vars)
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Cloud Run sends traffic to $PORT (default 8080)
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
