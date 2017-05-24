import logging
import uuid

from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.views.generic import View

from ..models import FlowCase
from ..models import FlowNote

logger = logging.getLogger(__name__)


class ApiCaseUpdateNoteView(AjaxResponseMixin, JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        response_dict = {}
        case_id = uuid.UUID(request.POST.get('case_id'))
        title = request.POST.get('title')
        content = request.POST.get('content')
        try:
            note_id = uuid.UUID(request.POST.get('note_id'))
        except:
            note_id = None
        flow_case = FlowCase.find_one(case_id)
        if (flow_case is not None):
            if note_id is not None:
                flow_note = FlowNote.find_one(note_id)
            else:
                flow_note = None

            if (flow_note is None):
                flow_note = FlowNote()
                flow_note.flow_case = flow_case

            flow_note.content = content
            flow_note.title = title

            flow_note.save()

        return self.render_json_response(response_dict)
