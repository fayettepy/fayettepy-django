import datetime
import json
import requests

from django.conf import settings
from django.views.generic import TemplateView

class IndexView(TemplateView):
    """
    View for the FayettePy homepage.
    """
    template_name = "index.html"


class MembersView(TemplateView):
    """
    This view lists FayettePy members via the Meetup API
    """
    template_name = "members.html"

    def get_context_data(self, **kwargs):
        """
        Get members from Meetup API
        """

        member_endpoint = "https://api.meetup.com/2/members/"

        params = {
            'sign': True,
            'key': settings.MEETUP_API_KEY,
            'group_urlname': settings.MEETUP_GROUP_URLNAME
        }
        response = requests.get(member_endpoint, params)
        api_members = json.loads(response.content)

        members = []
        for m in api_members['results']:
            members.append({
                'name': m.get('name', None),
                'photo': m.get('photo', None),
                'bio': m.get('bio', None),
            })

        kwargs.update({'members': members})
        return super(MembersView, self).get_context_data(**kwargs)


class EventsView(TemplateView):
    """
    This view lists upcoming events via the Meetup API
    """
    template_name = "events.html"

    def get_context_data(self, **kwargs):
        """
        Get Events from the Meetup API
        """
        events_endpoint = "https://api.meetup.com/2/events/"

        params = {
            'sign': True,
            'key': settings.MEETUP_API_KEY,
            'group_urlname': settings.MEETUP_GROUP_URLNAME
        }
        response = requests.get(events_endpoint, params)
        api_events = json.loads(response.content)

        events = []
        for e in api_events['results']:
            date = datetime.datetime.fromtimestamp(e.get('time', None) / 1000)

            events.append({
                'name': e.get('name', None),
                'url': e.get('event_url', None),
                'venue': e.get('venue', None),
                'date': date.strftime("%A, %B %d, %Y at %I:%S %p"),
                'description': e.get('description', None),
            })

        kwargs.update({'events': events})
        return super(EventsView, self).get_context_data(**kwargs)