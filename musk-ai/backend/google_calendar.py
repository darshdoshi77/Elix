from fastapi import APIRouter, HTTPException
import os
import pickle
from OpenAI import *
from googleapiclient.discovery import build
from datetime import datetime
import pytz

router = APIRouter()

@router.post("/create_event")
async def create_gc_event(request):
    event_function = {
    "name": "event_details",
    "description": "Extracts details for creating a calendar event.",
    "parameters": {
        "type": "object",
        "properties": {
            "summary": {
                "type": "string",
                "description": "The title of the event"
            },
            "start_time": {
                "type": "string",
                "description": "The start time in ISO format (YYYY-MM-DDTHH:MM:SS)"
            },
            "end_time": {
                "type": "string",
                "description": "The end time in ISO format (YYYY-MM-DDTHH:MM:SS)"
            },
            "timezone": {
                "type": "string",
                "description": "The time zone of the event",
                "default": "America/Los_Angeles"
            }
        },
        "required": ["summary", "start_time", "end_time","timezone"]
    }
} 
    context_str = "extract the relevant details regarding the event creation request"
    
    gpt_output = run_gpt_function_call(request, context_str, [event_function])
    print("GPT Output:", gpt_output)
    summary = gpt_output[0]['summary']
    start_time = gpt_output[0]['start_time']
    end_time = gpt_output[0]['end_time']
    timezone = gpt_output[0]['timezone']
       
    service = get_calendar_service()
          
    event = {
        "summary": summary,
        "start": {"dateTime": start_time, "timeZone": timezone},
        "end": {"dateTime": end_time, "timeZone": timezone},
        }
           
    service.events().insert(calendarId="primary", body=event).execute()
    return "Event created successfully"
    

@router.get("/check_availability")
async def check_gc_availability(request):
    
    availability_function = {
        "name": "availability_details",
        "description": "Extracts details for checking Google Calendar availability.",
        "parameters": {
            "type": "object",
            "properties": {
                "start_time": {
                    "type": "string",
                    "description": "The start time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)"
                },
                "end_time": {
                    "type": "string",
                    "description": "The end time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)"
                },
                "timezone": {
                    "type": "string",
                    "description": "The time zone of the event",
                    "default": "America/Los_Angeles"
                }
            },
            "required": ["start_time", "end_time", "timezone"]
        }
    }

    context_str = "Extract the relevant details to check availability"

    gpt_output = run_gpt_function_call(request, context_str, [availability_function])
    print("GPT Output:", gpt_output)
    
    start_time = gpt_output[0]['start_time']
    end_time = gpt_output[0]['end_time']
    timezone = gpt_output[0]['timezone']

    
    start_time_iso = f"{start_time}-08:00"  
    end_time_iso = f"{end_time}-08:00"

    print(f"Checking availability from {start_time_iso} to {end_time_iso} in timezone {timezone}")

    body = {
        "timeMin": start_time_iso,
        "timeMax": end_time_iso,
        "timeZone": timezone,
        "items": [{"id": "primary"}]
    }

    service = get_calendar_service()

    try:
        response = service.freebusy().query(body=body).execute()
        busy_slots = response.get("calendars", {}).get("primary", {}).get("busy", [])

        if busy_slots:
            formatted_busy_times = format_busy_slots(busy_slots)
            return f"Not Available, busy_slots: {formatted_busy_times}"
        
        return "Available"
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking availability: {str(e)}")

    
@router.delete("/delete_event")
async def delete_gc_event(request):
    delete_event_function = {
        "name": "delete_event_details",
        "description": "Extracts details for deleting a calendar event.",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "The title of the event to be deleted. DO NOT include the time, date and any other irrelevant information."
                }
            },
            "required": ["summary"]
        }
    }
    
    context_str = "Extract the relevant details regarding the event deletion request"
    gpt_output = run_gpt_function_call(request, context_str, [delete_event_function])
    event_title = gpt_output[0]['summary']
    print("gpt_output", event_title)
    
    if not event_title:
        raise HTTPException(status_code=400, detail="Event title is required")
    
    service = get_calendar_service()
    try:
        events_result = service.events().list(calendarId="primary").execute()
        events = events_result.get("items", [])
        
        matching_event = None
        for event in events:
            event_summary = event.get("summary")
            if event_summary and event_summary.lower() == event_title.lower():
                matching_event = event
                break

        if not matching_event:
            return "Event not found!"

        print(f"Deleting event: {matching_event.get('summary')} (ID: {matching_event['id']})")
        service.events().delete(calendarId="primary", eventId=matching_event["id"]).execute()

        return "Event deleted successfully"

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting event: {str(e)}")


def get_calendar_service():
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
            
        return build("calendar", "v3", credentials=creds)
    else:
        raise Exception("No token.pickle found! Run authentication script first.")


def convert_utc_to_pst(utc_time):
    utc = pytz.utc
    pst = pytz.timezone("America/Los_Angeles")

    dt_utc = datetime.fromisoformat(utc_time.replace("Z", "+00:00"))

    dt_pst = dt_utc.astimezone(pst)

    return dt_pst.strftime("%Y-%m-%d %I:%M %p %Z") 

def format_busy_slots(busy_slots):
    
    formatted_slots = []
    for slot in busy_slots:
        start_pst = convert_utc_to_pst(slot["start"])
        end_pst = convert_utc_to_pst(slot["end"])
        formatted_slots.append(f"{start_pst} to {end_pst}")

    return "\n".join(formatted_slots)