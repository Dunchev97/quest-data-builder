import json
from pathlib import Path
import tempfile
import unittest

from openpyxl import Workbook

from src import export_xlsx, workbench_addition, workflow_fast


class WorkbenchAdditionTests(unittest.TestCase):
    def table(self, path, rows, sheet="conf"):
        wb = Workbook()
        wb.active.title = sheet
        for row in rows:
            wb.active.append(row)
        wb.save(path)
        wb.close()

    def block(self, family, names):
        return [["sl", "string", "string", "string", "string"],
                [None, "input", "output", "classname", "title"],
                *[[None, "/recipe/Donor_Recipe.proto.js",
                   f"/{family}/Event_2026/{output}.proto.js", name, title]
                  for output, name, title in names], []]

    def entry(self, result):
        header, body = Path(result["txt"]).read_text(encoding="utf-8").split("\n\n", 1)
        self.assertEqual(header, workbench_addition.WORKBENCH_FILE)
        self.assertTrue(body.endswith("},\n"))
        return json.loads(body.rstrip()[:-1])

    def test_all_recipe_definitions_manual_names_natural_order_and_no_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            self.table(folder / "resources.xlsx", self.block("recipe", [
                ("Event_2026_R_10_Recipe", None, None),
                ("Event_2026_R_2_Recipe", None, None),
                ("Event_2026_R_1_Recipe", None, None)]))
            self.table(folder / "rewards.xlsx", self.block("recipe", [
                ("Event_2026_R_MB_1_Recipe", None, None),
                ("Event_2026_R_1_Recipe", None, None)]))
            self.table(folder / "interactive.xlsx", self.block("recipe", [
                ("Event_2026_Old_Recipe", "Event_2026_Exchanger_R_1_Recipe", None)]))
            self.table(folder / "quests.xlsx", self.block("quest_group", [
                ("Event_2026_Story", None, "Ручной заголовок")]))
            self.table(folder / "assets.xlsx", self.block("quest_item", [
                ("Event_2026_Referenced_Recipe", None, "Donor_Recipe")]), sheet="Conf")
            (folder / "~$lock.xlsx").write_bytes(b"Excel lock")
            before = {p: p.read_bytes() for p in folder.glob("*.xlsx")}
            result = workbench_addition.build("Event_2026", folder)
            entry = self.entry(result)
            self.assertEqual(entry, {
                "id": "Event_2026", "attention": "Изготавливать можно",
                "title": "Ручной заголовок", "icon": "Event_2026_R_1",
                "conditions": "active_quest_group=Event_2026_Tech",
                "recipes": ["Event_2026_Exchanger_R_1_Recipe", "Event_2026_R_1_Recipe",
                            "Event_2026_R_2_Recipe", "Event_2026_R_10_Recipe", "Event_2026_R_MB_1_Recipe"],
            })
            self.assertEqual(result["recipes"], 5)
            self.assertTrue(all(p.read_bytes() == data for p, data in before.items()))

    def test_writer_refreshes_added_recipe_and_unchanged_list_is_not_rewritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for n in (1, 2):
                rows = self.block("recipe", [(f"Event_2026_R_{n}_Recipe", None, None)])
                export_xlsx.write_workbook(folder / f"r{n}.xlsx",
                                          [export_xlsx.WorkbookSheet("conf", rows, "resource_table")],
                                          campaign_id="Event_2026")
            result = workbench_addition.build("Event_2026", folder)
            path = Path(result["txt"])
            self.assertEqual(result["recipes"], 2)
            stamp = path.stat().st_mtime_ns
            workbench_addition.build("Event_2026", folder)
            self.assertEqual(stamp, path.stat().st_mtime_ns)
            self.table(folder / "r2.xlsx", self.block("recipe", [("Event_2026_New_Recipe", None, None)]))
            self.assertEqual(workflow_fast.main(["workbench-addition", "--campaign", "Event_2026",
                                                "--pack", "pack_001", "--tables-dir", str(folder)]), 0)
            self.assertEqual(self.entry(result)["recipes"], ["Event_2026_New_Recipe", "Event_2026_R_1_Recipe"])

    def test_invalid_manual_names_fail_before_overwriting_existing_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            self.table(folder / "r.xlsx", self.block("recipe", [("Event_2026_R_1_Recipe", None, None)]))
            path = Path(workbench_addition.build("Event_2026", folder)["txt"])
            before = path.read_bytes()
            for name in ("Donor_Recipe", "=D4"):
                self.table(folder / "r.xlsx", self.block("recipe", [("Event_2026_R_1_Recipe", name, None)]))
                with self.assertRaisesRegex(ValueError, "invalid or foreign"):
                    workbench_addition.build("Event_2026", folder)
                self.assertEqual(path.read_bytes(), before)

    def test_empty_set_and_missing_workbooks(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            with self.assertRaisesRegex(ValueError, "No XLSX"):
                workbench_addition.build("Event_2026", folder)
            self.table(folder / "r.xlsx", self.block("quest_item", [("Event_2026_R_1", None, None)]))
            self.assertEqual(self.entry(workbench_addition.build("Event_2026", folder))["recipes"], [])


if __name__ == "__main__":
    unittest.main()
