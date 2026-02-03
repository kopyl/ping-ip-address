# Description

A Dockerized application that
- Pings a specified IP address and port for availability.
- Sends notifications via Telegram if the IP address is unreachable.

### Tech Stack:
- Python
- Docker
- Supabase (PostgreSQL)
- Oracle (for VPS hosting)

#### Build for development:
```sh
docker build -t ping-ip-address .
```

### Build for AMD64 architecture on Apple Silicon:
```sh
docker build --platform linux/amd64/v2 -t ping-ip-address .
```

### Docker run;
```sh
docker run --rm \
    -e PING_IP_ADDRESS="0.0.0.0" \
    -e PING_PORT="80" \
    -e TELEGRAM_BOT_TOKEN="XXX" \
    -e TELEGRAM_CHAT_ID="-100" \
    -e SUPABASE_SERVICE_KEY="sb_secret_..." \
    -e SUPABASE_PROJECT_ID="..." \
    ping-ip-address
```


### Push to Docker Hub:
```sh
docker tag ping-ip-address kopyl/ping-ip-address:latest
docker push kopyl/ping-ip-address:latest
```

### Requirements:
- Data API on Supabase must be enabled in project settings
- RLS must be enabled in project settings
- [Disable IP accessing via client libraries](PostgreSQL/functions/check_ip)
- Docker installed

#### Database tables required:
- ping_statuses

#### Database table columns required:
- id
  - Type: uuid
  - Default value: gen_random_uuid()
  - Generated on insert: yes
- created_at
  - Type: timestampz (timestamp with a time zone)
  - Default value: now()
- status
  - Type: bool
- ip_address
  - Type: text
- port
  - Type: int2

#### Column properties:
- Applied to all:
    - Not nullable
    - Not unique
        - Exception:
            - id
    - Not defined as Array