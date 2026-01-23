
from dataclasses import dataclass, field
from typing import Optional, List


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
    date: Optional[str] = None
    file_name: str
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

def new_sermon_draft(code: str) -> SermonDraft:
    return SermonDraft(
        code=code,
        title=''
    )

def new_service_draft(date: str = None) -> ServiceDraft:
    return ServiceDraft(
        date=date,
        place=''
    )

def new_manuscript_draft() -> ManuscriptDraft:
    return ManuscriptDraft(
        file_name=''
    )

def new_recording_draft() -> RecordingDraft:
    return RecordingDraft(
        date='',
        type=''
    )

def new_resource_draft() -> ResourceDraft:
    return ResourceDraft(
        file_name=''
    )



