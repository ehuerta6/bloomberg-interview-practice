class DocumentRepository:
    def __init__(self): self.folders={}; self.documents={}
    def add_folder(self,folder): self.folders[folder.folder_id]=folder
    def add_document(self,doc): self.documents[doc.document_id]=doc
    def document(self,doc_id): return self.documents.get(doc_id)
