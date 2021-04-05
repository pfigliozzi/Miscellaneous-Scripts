"""
This script will delete Cubs away games from your Google calendar if you subscribed to
the official MLB calendar. The script utilizes the google calendar api through the 
Google Client api.

Documentation at https://developers.google.com/calendar/quickstart/python can help
you get started adding yourself as a developer and pip installing the Google Client api.

This script expects the credentials.json object in the same directory in order to 
authenticate connecting to Google api. 
"""

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# The name of the calendar that contains the events you want to delete.
CALENDAR_NAME = 'Chicago Cubs Schedule'

# Every Cubs home game begins with this string. Used to find events to delete.
EVENT_FILTER_STRING = '⚾️ Chicago Cubs'

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the calendar API to get the id of CALENDAR_NAME
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])
    filtered_calendars = next(filter(lambda x: x['summary'] == CALENDAR_NAME, calendars))
    calendar_id = filtered_calendars['id']
   
    # Delete all events from the calendar the start with EVENT_FILTER_STRING
    events_result = service.events().list(calendarId=calendar_id).execute()
    events_to_delete =[event for event in events_result['items'] if event['summary'].startswith(EVENT_FILTER_STRING)]
    for event in events_to_delete:
        service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()
        print('Deleted {} on {}'.format(event['summary'], event['start']['dateTime']))

if __name__ == '__main__':
    main()
