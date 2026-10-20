from dataclasses import dataclass, field

@dataclass
class Folder:
    folder_id: str
    parent_id: str | None = None
    grants: dict = field(default_factory=dict)
    revoked: set = field(default_factory=set)

@dataclass
class Document:
    document_id: str
    folder_id: str
    owner: str
    grants: dict = field(default_factory=dict)
    revoked: set = field(default_factory=set)
