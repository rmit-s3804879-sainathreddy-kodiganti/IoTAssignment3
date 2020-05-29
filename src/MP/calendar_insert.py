import pickle
from googleapiclient import discovery
from datetime import datetime, timedelta


class CalendarUtil():
    """This is the CalendarUtil Class

    This is used to create calendar Events
    """

    def addToCalendar(self, email, start_time, end_time, summary):
        """This function reads the credentials saved in the pickle file and creats a calendar event.

        :param: email, start_time, end_time, summary 
        :return: (bool) True if calendar event is created
        """
        try:
            credentials = pickle.load(open("token.pkl", "rb"))
            service = discovery.build(
                "calendar", "v3", credentials=credentials)
            timezone = 'Australia/Victoria'
            location = 'Victoria'
            description = 'Car Booking'
            result = service.calendarList().list().execute()
            calendar_id = result['items'][0]['id']
            event = self.getEvent(email, start_time, end_time, summary,
                                  location, description, timezone)
            ev = service.events().insert(calendarId=calendar_id, body=event).execute()
            return ev
        except Exception as ex:
            return None


    def deleteFromCalendar(self, event_id):
        """This function reads the credentials saved in the pickle file and creats a calendar event.

        :param: email, start_time, end_time, summary 
        :return: (bool) True if calendar event is created
        """
        try:
            credentials = pickle.load(open("token.pkl", "rb"))
            service = discovery.build(
                "calendar", "v3", credentials=credentials)
            result = service.calendarList().list().execute()
            calendar_id = result['items'][0]['id']

            resp = service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
            print(resp)
        except Exception as ex:
            print(ex)
            return False
        return True


    def getEvent(self, email, start_time, end_time, summary, location, description, timezone):
        """This function creats a event object.

        :param: start_time, end_time, summary, location, description, timezone 
        :return: (object) event
        """
        return {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'attendees': [{
                'email': email
            }],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
