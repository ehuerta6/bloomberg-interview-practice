class PermissionService:
    LEVEL={"viewer":1,"editor":2,"owner":3}
    def __init__(self,repo): self.repo=repo
    def grant_folder(self,folder_id,user,role):
        if folder_id not in self.repo.folders or role not in ("viewer","editor"): raise ValueError("invalid grant")
        folder=self.repo.folders[folder_id]; folder.grants[user]=role; folder.revoked.discard(user)
    def grant_document(self,doc_id,user,role):
        doc=self.repo.document(doc_id)
        if not doc or role not in ("viewer","editor"): raise ValueError("invalid grant")
        doc.grants[user]=role; doc.revoked.discard(user)
    def revoke(self,doc_id,user):
        doc=self.repo.document(doc_id)
        if not doc or user==doc.owner: raise ValueError("cannot revoke")
        doc.revoked.add(user)
    def role(self,doc_id,user):
        doc=self.repo.document(doc_id)
        if not doc: return None
        if user==doc.owner: return "owner"
        if user in doc.revoked: return None
        if user in doc.grants: return doc.grants[user]
        folder=self.repo.folders.get(doc.folder_id); visited=set()
        while folder and folder.folder_id not in visited:
            visited.add(folder.folder_id)
            if user in folder.revoked: return None
            if user in folder.grants: return folder.grants[user]
            folder=self.repo.folders.get(folder.parent_id) if folder.parent_id else None
        return None
    def can(self,doc_id,user,action):
        role=self.role(doc_id,user)
        needed={"read":1,"edit":2,"share":3}.get(action)
        return role is not None and needed is not None and self.LEVEL[role]>=needed
