from django.conf import settings
from google.oauth2 import credentials

from googleapiclient.discovery import build


class GoogleAnalyticsClient:

    def __init__(
            self,
            access_token,
            refresh_token=None,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            client_secret=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            quota_project_id=settings.QUOTA_PROJECT_ID,
    ):
        self.Credentials = credentials.Credentials(
            access_token,
            refresh_token=refresh_token,
            token_uri=token_uri,
            client_id=client_id,
            client_secret=client_secret,
            quota_project_id=quota_project_id,
        )
        self.Analytics = build('analyticsreporting', 'v4', credentials=self.Credentials)

    def get_goal_value(self, view_id, start_date: str = '7daysAgo', end_date: str = 'today'):
        result = []
        response = self.Analytics.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': view_id,
                        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                        'metrics': [{'expression': 'ga:goalValueAll'}],
                        'dimensions': [{'name': 'ga:medium'}, {'name': 'ga:source'}, {'name': 'ga:campaign'}],
                    }]
            }
        ).execute()
        for row in response.get("reports", [{}])[0].get("data", {}).get("rows", []):
            result.append(dict(
                medium=row.get("dimensions", [''])[0],
                source=row.get("dimensions", ['', ''])[1],
                campaign=row.get("dimensions", ['', '', ''])[2],
                value=row.get("metrics", [{}])[0].get("values", ['0'])[0]
            ))
        return result
