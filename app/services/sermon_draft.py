
from dataclasses import dataclass, field
from typing import Optional, List
import copy

@dataclass
class SermonDraft:
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
    date: str
    place: str
    notes: Optional[str] = None


@dataclass
class ManuscriptDraft:
    file_name: str
    date: Optional[str] = None
    version: Optional[int] = None
    notes: Optional[str] = None

@dataclass
class RecordingDraft:
    date: str
    type: str
    file_name: Optional[str] = None
    external_url: Optional[str] = None
    notes: Optional[str] = None

@dataclass
class ResourceDraft:
    file_name: str
    title: Optional[str] = None
    notes: Optional[str] = None




# Helpfunctions for creating empty drafts

def new_sermon_draft(template = None) -> SermonDraft:
    if template:  # A draft with data from a template
        return SermonDraft(
            code=template['code'],
            title=template['title'],
            context=template['context'],
            introduction=template['introduction'],
            message=template['message'],
            report=template['report'],
            notes=template['notes']
        )
    else:  # An empty draft
        return SermonDraft(
            code='',
            title=''
        )

def new_service_draft(template = None) -> ServiceDraft:
    if template:
        return ServiceDraft(
            date=template['date'],
            place=template['place'],
            notes=template['notes']
        )
    else:
        return ServiceDraft(
            date='',
            place=''
        )

def new_manuscript_draft(template = None) -> ManuscriptDraft:
    if template:
        return ManuscriptDraft(
            file_name=template['file_name'],
            date=template['date'],
            version=template['version'],
            notes=template['notes']
        )
    else:
        return ManuscriptDraft(
            file_name=''
        )

def new_recording_draft(template = None) -> RecordingDraft:
    if template:
        return RecordingDraft(
            date=template['date'],
            type=template['type'],
            file_name=template['file_name'],
            external_url=template['external_url'],
            notes=template['notes'],
        )
    else:
        return RecordingDraft(
            date='',
            type=''
        )

def new_resource_draft(template = None) -> ResourceDraft:
    if template:
        return ResourceDraft(
            file_name=template['file_name'],
            title=template['title'],
            notes=template['notes'],
        )
    else:
        return ResourceDraft(
            file_name=''
        )


def deep_copy(draft: sermonDraft):
    """Make a deep copy of a sermon draft."""
    return copy.deepcopy(draft)



