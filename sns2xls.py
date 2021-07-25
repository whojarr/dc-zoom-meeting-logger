import os
import json
import google_sheet


GOOGLE_SHEET_NAME = os.environ['GOOGLE_SHEET_NAME']


def google_sheet_write_participant(meeting):
    pass


def event_meeting(event):

    if 'Records' in event:
        for record in event['Records']:
            if record['EventSource'] == 'aws:sns':
                subject = record['Sns']['Subject']
                message = json.loads(record['Sns']['Message'])
                event = message['event']
                account_id = message['payload']['account_id']
                obj = message['payload']['object']

                if not 'end_time' in obj:
                    obj['end_time'] = ''

                result = {
                        "topic": obj['topic'],
                        "event": event,
                        "timezone": obj['timezone'],
                        "start_time": obj['start_time'],
                        "end_time": obj['end_time'],
                        "duration": obj['duration'],
                        "account_id": account_id,
                        "host_id": obj['host_id'],
                        "subject": subject,
                        "type": obj['type'],
                        "id": obj['id'],
                        "uuid": obj['uuid']
                    }

                if 'participant' in obj:
                    if not 'join_time' in obj['participant']:
                        obj['participant']['join_time'] = ""
                    if not 'leave_time' in obj['participant']:
                        obj['participant']['leave_time'] = ""
                    result['user_name'] = obj['participant']['user_name']
                    result['email'] = obj['participant']['email']
                    result['join_time'] = obj['participant']['join_time']
                    result['leave_time'] = obj['participant']['leave_time']
                    result['user_id'] = obj['participant']['user_id']
                    result['participant_id'] = obj['participant']['id']

                yield result


def handler(event, context):

    for meeting in event_meeting(event):

        meeting_event = meeting['event']
        worksheet_name = meeting['topic']
        if meeting_event == 'meeting.started' or meeting_event == 'meeting.ended':
            meeting_values = meeting.values()
            meeting_row = list(meeting_values) 
            result = google_sheet.googlesheet_update(GOOGLE_SHEET_NAME, worksheet_name, meeting_row)
        elif meeting_event == 'meeting.participant_joined' or meeting_event == 'meeting.participant_left':
            meeting_participant_values = meeting.values()
            meeting_participant_row = list(meeting_participant_values) 
            result = google_sheet.googlesheet_update(GOOGLE_SHEET_NAME, worksheet_name, meeting_participant_row)

        print(result)


