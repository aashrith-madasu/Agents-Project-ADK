GOOGLE_CLOUD_PROJECT="learning-adk-462618"
GOOGLE_CLOUD_LOCATION="us-central1"
SERVICE_NAME="weather-bot-service"
AGENT_PATH="./weather_bot"
APP_NAME="weather-bot-app"

adk deploy cloud_run \
    --project=$GOOGLE_CLOUD_PROJECT \
    --region=$GOOGLE_CLOUD_LOCATION \
    --service_name=$SERVICE_NAME \
    --app_name=$APP_NAME \
    --with_ui \
    $AGENT_PATH