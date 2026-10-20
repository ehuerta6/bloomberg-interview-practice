import unittest
from repository import CustomerRepository
from service import ImportService
from routes import ImportRoutes

class ImportTests(unittest.TestCase):
    def setUp(self): self.repo=CustomerRepository(); self.service=ImportService(self.repo); self.routes=ImportRoutes(self.service)
    def test_valid_rows_commit_independently_despite_bad_neighbor(self):
        result=self.routes.post([{"id":"a","email":"A@x.test","amount":"5"},{"id":"b","email":"broken","amount":"2"},{"id":"c","email":"c@x.test","amount":"0"}])
        self.assertEqual(result["status"],207); self.assertEqual(result["accepted"],["a","c"]); self.assertEqual(set(self.repo.records),{"a","c"})
    def test_duplicate_in_batch_is_reported_without_overwriting_first(self):
        result=self.service.import_rows([{"id":"a","email":"a@x.test","amount":1},{"id":"a","email":"new@x.test","amount":9}])
        self.assertEqual(result["accepted"],["a"]); self.assertEqual(self.repo.get("a").email,"a@x.test"); self.assertEqual(len(result["errors"]),1)
    def test_duplicate_existing_record_does_not_overwrite(self):
        self.service.import_rows([{"id":"a","email":"a@x.test","amount":1}])
        result=self.service.import_rows([{"id":"a","email":"other@x.test","amount":2}])
        self.assertEqual(result["accepted"],[]); self.assertEqual(self.repo.get("a").amount,1)
    def test_normalizes_email_and_rejects_invalid_numbers(self):
        result=self.service.import_rows([{"id":"x","email":" X@EXAMPLE.TEST ","amount":"8"},{"id":"y","email":"y@x.test","amount":-1},{"id":"z","email":"z@x.test","amount":1.5}])
        self.assertEqual(self.repo.get("x").email,"x@example.test"); self.assertEqual([e["row"] for e in result["errors"]],[2,3])
    def test_top_level_payload_validation(self): self.assertEqual(self.routes.post({})["status"],400)

class AdditionalImportTests(unittest.TestCase):
    def test_boolean_amount_is_not_an_integer_amount(self):
        repo=CustomerRepository(); service=ImportService(repo)
        result=service.import_rows([{"id":"a","email":"a@x.test","amount":True}])
        self.assertEqual(result["accepted"],[]); self.assertEqual(repo.records,{})
    def test_missing_fields_are_reported_and_later_rows_continue(self):
        repo=CustomerRepository(); result=ImportService(repo).import_rows([{}, {"id":"ok","email":"ok@x.test","amount":"4"}])
        self.assertEqual(result["accepted"],["ok"]); self.assertEqual(result["errors"][0]["row"],1)


if __name__=="__main__": unittest.main()
