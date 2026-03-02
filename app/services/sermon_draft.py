
from dataclasses import dataclass, field, asdict
from typing import Optional, List
import copy, re
from app.utils import get_last_sunday, PATTERN
from app.db import get_sermon_by_code, get_services_for_sermon, get_manuscripts_for_sermon, get_recordings_for_sermon, get_resources_for_sermon, get_bible_references_for_sermon, get_related_sermons_for_sermon, create_sermon_in_database
from app.errors import ValidationError



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
    """Fetch a sermon and return as a draft."""

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


def create_sermon_from_draft(draft: SermonDraft):
    """Create a sermon in the database from the draft."""
    validate_sermon_draft(draft)  # This validation function throws errors if something is wrong in the draft
    create_sermon_in_database(draft)  # Insert this sermon in the database


def validate_sermon_draft(draft: SermonDraft):
    """Throw an error if something is wrong in the sermon draft."""

    if not PATTERN['code'].match(draft.code):
        raise ValidationError(f"Predikokod måste vara i formatet [key]P001[/key]. ([error]{draft.code}[/error])")

    if not draft.title or not draft.title.strip():
        raise ValidationError('Titel får inte vara tom.')

    if draft.report not in ('A', 'B', 'C', '', None):
        raise ValidationError(f"Omdöme måste vara [key]A[/key], [key]B[/key], [key]C[/key], eller tomt. ([error]{draft.report}[/error])")

    for service in draft.services:
        if not PATTERN['date'].match(service.date):
            raise ValidationError(f"Datum för gudstjänst är ogiltigt. ([error]{service.date}[/error])")
        if not service.place or not service.place.strip():
            raise ValidationError('Plats för gudstjänst får inte vara tom.')

    for manuscript in draft.manuscripts:
        if not PATTERN['manuscript'].match(manuscript.file_name):
            raise ValidationError(f"Filnamnet för manus är felaktigt. ([error]{manuscript.file_name}[/error])")

    for recording in draft.recordings:
        if not PATTERN['date'].match(recording.date):
            raise ValidationError(f"Datum för inspelning är ogiltigt. ([error]{recording.date}[/error])")
        if recording.type not in ('audio', 'video'):
            raise ValidationError('Typ för inspelning måste vara [key]audio[/key] eller [key]video[/key].')
        if not (recording.file_name or recording.external_url):
            raise ValidationError('Filnamn eller extern url måste anges för inspelning.')
        if recording.file_name and recording.external_url:
            raise ValidationError('Både filnamn och url har angetts för inspelning, endast en kan anges per inspelning.')
        if recording.file_name:
            if not PATTERN['recording'].match(recording.file_name):
                raise ValidationError(f"Ange filnamn för inspelning enligt standardformatet: [key]{get_last_sunday()}_Predikan.mp3[/key] ([error]{recording.file_name}[/error])")
        if recording.external_url:
            if not PATTERN['url'].match(recording.external_url):
                raise ValidationError(f"Extern url för inspelning förefaller inte vara en giltig url. ([error]{recording.external_url}[/error])")

    for resource in draft.resources:
        if not PATTERN['file_name'].match(resource.file_name):
            raise ValidationError(f"Filnamnet för en resurs är felaktigt. ([error]{resource.file_name}[/error])")

    if draft.code in draft.related_sermons:
        raise ValidationError('Predikan kan inte relateras till sig själv.')




def deep_copy(draft: sermonDraft):
    """Make a deep copy of a sermon draft."""
    return copy.deepcopy(draft)


def equal_drafts(draft1: sermonDraft, draft2: sermonDraft):
    """Compare if the two drafts are equal or not"""
    d1 = asdict(draft1)
    d2 = asdict(draft2)
    return d1 == d2






