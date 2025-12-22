# Frontend Dockerfile - React/Vite Application
# Multi-stage build for smaller final image

# Stage 1: Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first for better layer caching
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci --legacy-peer-deps

# Copy source code
COPY . .

# Set API URL for production build
ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}

# Build the application
RUN npm run build

# Stage 2: Production stage with nginx
FROM nginx:alpine

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Create non-root user for security
RUN addgroup -g 1001 -S nginx-group \
    && adduser -u 1001 -S nginx-user -G nginx-group \
    && chown -R nginx-user:nginx-group /usr/share/nginx/html \
    && chown -R nginx-user:nginx-group /var/cache/nginx \
    && chown -R nginx-user:nginx-group /var/log/nginx \
    && touch /var/run/nginx.pid \
    && chown -R nginx-user:nginx-group /var/run/nginx.pid

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:80/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
