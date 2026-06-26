FROM node:20-alpine AS build
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

FROM python:3.11-alpine
WORKDIR /app
COPY server.py .
COPY --from=build /app/dist ./static
EXPOSE 5000
CMD ["python", "server.py"]
