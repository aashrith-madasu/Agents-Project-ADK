PORT=8000

# Build
# docker build -t my-agent-app .

# Run
docker run -d -p 0.0.0.0:3000:$PORT -e "PORT=$PORT" my-agent-app