GOOGLE_CLOUD_PROJECT="learning-adk-462618"
GOOGLE_CLOUD_LOCATION="us-central1"
SERVICE_NAME="weather-bot-service"
AGENT_PATH="./weather_bot"
APP_NAME="weather-bot-app"

# adk deploy cloud_run \
#     --project=$GOOGLE_CLOUD_PROJECT \
#     --region=$GOOGLE_CLOUD_LOCATION \
#     --service_name=$SERVICE_NAME \
#     --app_name=$APP_NAME \
#     --with_ui \
#     $AGENT_PATH

gcloud run deploy $SERVICE_NAME \
--source . \
--region $GOOGLE_CLOUD_LOCATION \
--project $GOOGLE_CLOUD_PROJECT \
--allow-unauthenticated \
--set-env-vars="GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT,\
                GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION,\
                GOOGLE_GENAI_USE_VERTEXAI=$GOOGLE_GENAI_USE_VERTEXAI,\
                GOOGLE_API_KEY=$GOOGLE_API_KEY,\
                WEAVIATE_REST_ENDPOINT=$WEAVIATE_REST_ENDPOINT,\
                WEAVIATE_API_KEY=$WEAVIATE_API_KEY"
# Add any other necessary environment variables your agent might need