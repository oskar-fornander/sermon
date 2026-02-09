
from dataclasses import dataclass, field, asdict
from typing import Optional, List
import copy
from app.utils import get_last_sunday


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


def deep_copy(draft: sermonDraft):
    """Make a deep copy of a sermon draft."""
    return copy.deepcopy(draft)


def equal_drafts(draft1: sermonDraft, draft2: sermonDraft):
    """Compare if the two drafts are equal or not"""
    d1 = asdict(draft1)
    d2 = asdict(draft2)
    return d1 == d2






