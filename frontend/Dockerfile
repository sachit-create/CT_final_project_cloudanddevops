# Use an official Nginx image to serve static files.
FROM nginx:1.27-alpine

# Copy custom Nginx config that proxies /api to backend service.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy frontend static dashboard page.
COPY index.html /usr/share/nginx/html/index.html

# Document container listening port.
EXPOSE 80
