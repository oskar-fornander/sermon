
from dataclasses import dataclass, field, asdict
from typing import Optional, List
import copy
from app.utils import get_last_sunday
from app.db import get_sermon_by_code, get_services_for_sermon, get_manuscripts_for_sermon, get_recordings_for_sermon, get_resources_for_sermon, get_bible_references_for_sermon, get_related_sermons_for_sermon


@dataclass
class SermonDraft:
    id: int  # Database id for saving
    code: str
    title: str
    context: Optional[str] = None
    introduction: Optional[str] = None
    message: Optional[str] = None
    report: Optional[str] = None
    notes: Optional[str] = None

    services: List['ServiceDraft'] = field(default_factory=list)
    manuscripts: List['ManuscriptDraft'] = field(default_factory=list)
    recordings: List['RecordingDraft'] = field(default_factory=list)
    resources: List['ResourceDraft'] = field(default_factory=list)
    bible_references: List[str] = field(default_factory=list)
    related_sermons: List[str] = field(default_factory=list)


@dataclass
class ServiceDraft:
    id: int  # Database id for saving
    date: str
    place: str
    notes: Optional[str] = None


@dataclass
class ManuscriptDraft:
    id: int  # Database id for saving
    file_name: str
    date: Optional[str] = None
    notes: Optional[str] = None

@dataclass
class RecordingDraft:
    id: int  # Database id for saving
    date: str
    type: str
    file_name: Optional[str] = None
    external_url: Optional[str] = None
    notes: Optional[str] = None

@dataclass
class ResourceDraft:
    id: int  # Database id for saving
    file_name: str
    title: Optional[str] = None
    notes: Optional[str] = None




# Helpfunctions for creating empty drafts

def new_sermon_draft(template = None) -> SermonDraft:
    if template:  # A draft with data from a template
        return SermonDraft(
            id=template['id'],
            code=template['code'],
            title=template['title'],
            context=template['context'],
            introduction=template['introduction'],
            message=template['message'],
            report=template['report'],
            notes=template['notes'],
            services=[],
            manuscripts=[],
            recordings=[],
            resources=[],
            bible_references=[],
            related_sermons=[]
        )
    else:  # An empty draft
        return SermonDraft(
            id = None,
            code='',
            title=''
        )

def new_service_draft(template = None, sermon_code='') -> ServiceDraft:
    if template:
        return ServiceDraft(
            id=template['id'],
            date=template['date'],
            place=template['place'],
            notes=template['notes']
        )
    else:
        return ServiceDraft(
            id = None,
            date=get_last_sunday(),
            place='–'
        )

def new_manuscript_draft(template = None, sermon_code='') -> ManuscriptDraft:
    if template:
        return ManuscriptDraft(
            id=template['id'],
            file_name=template['file_name'],
            date=template['date'],
            notes=template['notes']
        )
    else:
        return ManuscriptDraft(
            id = None,
            file_name=f"{sermon_code}.pdf",
            date=get_last_sunday()
        )

def new_recording_draft(template = None, sermon_code='') -> RecordingDraft:
    if template:
        return RecordingDraft(
            id=template['id'],
            date=template['date'],
            type=template['type'],
            file_name=template['file_name'],
            external_url=template['external_url'],
            notes=template['notes'],
        )
    else:
        return RecordingDraft(
            id = None,
            date=get_last_sunday(),
            file_name=f"{get_last_sunday()}_Predikan.mp3",
            type='audio'
        )

def new_resource_draft(template = None, sermon_code='') -> ResourceDraft:
    if template:
        return ResourceDraft(
            id=template['id'],
            file_name=template['file_name'],
            title=template['title'],
            notes=template['notes'],
        )
    else:
        return ResourceDraft(
            id = None,
            file_name=f"{sermon_code}_resurs.pdf"
        )


def load_sermon_as_draft(sermon_code: str) -> sermonDraft:
    """Hämta data om en predikan och returnera som ett draft."""

    # Get data from the database
    sermon = get_sermon_by_code(sermon_code)
    if not sermon:
        return None
    services = get_services_for_sermon(sermon_code)
    manuscripts = get_manuscripts_for_sermon(sermon_code)
    recordings = get_recordings_for_sermon(sermon_code)
    resources = get_resources_for_sermon(sermon_code)
    bible_references = get_bible_references_for_sermon(sermon_code)
    related_sermons = get_related_sermons_for_sermon(sermon_code)

    # Convert that data into a sermonDraft
    sermon_draft = new_sermon_draft(sermon)  # Create a new sermonDraft with data from the given sermon
    sermon_draft.services = [new_service_draft(s) for s in services]  # The same for all sub tables (some may be more than one element in a list)
    sermon_draft.manuscripts = [new_manuscript_draft(m) for m in manuscripts]
    sermon_draft.recordings = [new_recording_draft(r) for r in recordings]
    sermon_draft.resources = [new_resource_draft(r) for r in resources]
    #sermon_draft.bible = '; '.join([b['reference_text'] for b in bible_references])  # text
    #sermon_draft.related = ', '.join([s['code'] for s in related_sermons])
    sermon_draft.bible_references = [b['reference_text'] for b in bible_references]  # list
    sermon_draft.related_sermons = [s['code'] for s in related_sermons]

    return sermon_draft





def deep_copy(draft: sermonDraft):
    """Make a deep copy of a sermon draft."""
    return copy.deepcopy(draft)


def equal_drafts(draft1: sermonDraft, draft2: sermonDraft):
    """Compare if the two drafts are equal or not"""
    d1 = asdict(draft1)
    d2 = asdict(draft2)
    return d1 == d2






