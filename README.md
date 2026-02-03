#### Build for development:
docker build -t ping-ip-address .

### Build for AMD64 architecture on Apple Silicon:
docker build --platform linux/amd64/v2 -t ping-ip-address .

### Docker run;
docker run --rm \
    -e PING_IP_ADDRESS="0.0.0.0" \
    -e PING_PORT="80" \
    -e TELEGRAM_BOT_TOKEN="XXX" \
    -e TELEGRAM_CHAT_ID="-100" \
    -e SUPABASE_SERVICE_KEY="sb_secret_..." \
    -e SUPABASE_PROJECT_ID="..." \
    ping-ip-address


### Push to Docker Hub:
docker tag ping-ip-address kopyl/ping-ip-address:latest
docker push kopyl/ping-ip-address:latest