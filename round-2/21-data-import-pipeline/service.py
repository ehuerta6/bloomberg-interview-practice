from models import ImportRow

class ImportService:
    def __init__(self,repo): self.repo=repo
    @staticmethod
    def parse(raw):
        try: return ImportRow(raw["id"].strip(),raw["email"].strip().lower(),int(raw["amount"]))
        except (KeyError,AttributeError,TypeError,ValueError): return None
    def import_rows(self,rows):
        accepted=[]; errors=[]; seen=set()
        for index,raw in enumerate(rows,1):
            row=self.parse(raw)
            if row is None or not row.external_id or "@" not in row.email or row.amount<0:
                errors.append({"row":index,"reason":"invalid row"}); continue
            if row.external_id in seen:
                errors.append({"row":index,"reason":"duplicate id in file"}); continue
            seen.add(row.external_id)
            if self.repo.get(row.external_id):
                errors.append({"row":index,"reason":"already imported"}); continue
            self.repo.save(row); accepted.append(row.external_id)
        return {"accepted":accepted,"errors":errors}
