# Use an official Nginx image to serve static files.
FROM nginx:1.27-alpine

# Copy the custom Nginx configuration.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy frontend static assets.
COPY index.html /usr/share/nginx/html/index.html

# Document the container port Nginx listens on.
EXPOSE 80
