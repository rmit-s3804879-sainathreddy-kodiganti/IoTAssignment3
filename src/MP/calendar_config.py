from googleapiclient import discovery
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle


class CalendarConfig():
    """This is the CalendarConfig Class

    This is used to configure calendar
    """

    def setupCalendar(self):
        """This is the CalendarConfig Class

        This is used to setup calendar
        """
        try:
            scopes = ['https://www.googleapis.com/auth/calendar']
            flow = InstalledAppFlow.from_client_secrets_file(
                "src/MP/client_secret.json", scopes=scopes)
            credentials = flow.run_console()

            pickle.dump(credentials, open("token.pkl", "wb"))
            credentials = pickle.load(open("token.pkl", "rb"))
            service = discovery.build(
                "calendar", "v3", credentials=credentials)

            result = service.calendarList().list().execute()
            result['items'][0]

            calendar_id = result['items'][0]['id']
            result = service.events().list(calendarId=calendar_id,
                                           timeZone="Australia/Victoria").execute()
            result['items'][0]
        except:
            return False
        return True
