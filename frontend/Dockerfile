# --- Build Stage ---
FROM node:18-alpine AS build
WORKDIR /app


# Install dependencies
COPY package*.json ./
RUN npm install


# Copy source code
COPY . .


# Set build-time argument and environment variable for API URL
ARG API_URL=https://cranes.wahet-elarab.com
ENV VITE_API_URL=$API_URL


# Build for production
RUN npm run build



# --- Export Stage (for Caddy) ---
FROM alpine:3.19
WORKDIR /dist


# Copy the built frontend files into this stage
COPY --from=build /app/dist .


# Keep container alive only to expose /dist through a volume
CMD ["sh", "-c", "echo 'Frontend dist ready'; tail -f /dev/null"]
