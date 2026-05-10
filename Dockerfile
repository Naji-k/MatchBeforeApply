# Stage 1: Build SvelteKit & Caddy
FROM node:22-slim AS builder

RUN apt-get update && apt-get install -y curl \
    && curl -L "https://github.com/caddyserver/caddy/releases/download/v2.8.4/caddy_2.8.4_linux_amd64.tar.gz" | tar -xz -C /usr/local/bin/ \
    && apt-get clean

WORKDIR /app/publish

# Copy frontend code
COPY publish/package*.json ./
RUN npm ci 

COPY publish/ .

# Build SvelteKit (outputs to build/ directory)
RUN npm run build

# Stage 2: Build Python backend
FROM python:3.11-slim

WORKDIR /app

# Copy built SvelteKit from builder stage
COPY --from=builder /app/publish/build ./publish/build
COPY --from=builder /usr/local/bin/caddy /usr/local/bin/caddy

# Copy backend code
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend

# Copy Caddyfile
COPY Caddyfile /app/

# Create startup script
RUN echo '#!/bin/bash\n\
caddy run --config /app/Caddyfile &\n\
cd /app/backend && uvicorn main:app --host 0.0.0.0 --port 8000' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

ENV PORT=8080

CMD ["/entrypoint.sh"]
