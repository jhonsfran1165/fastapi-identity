import os
from app.core.config import settings

from google.cloud import bigquery
from google.oauth2 import service_account

BIGQUERY_CREDENTIALS = os.path.join(
    settings.BASE_DIR,
    settings.BIGQUERY_CREDENTIALS_FILE
)

credentials = service_account.Credentials.from_service_account_file(BIGQUERY_CREDENTIALS)

class BigQuery():
    def __init__(self):
        self.client = bigquery.Client(credentials=credentials, project=settings.BIGQUERY_PROJECT_ID)


bigquery = BigQuery()