import json
from pathlib import Path
import tempfile
import unittest

from openpyxl import Workbook

from src import export_xlsx, package_list


class PackageListTests(unittest.TestCase):
    def table(self, path, definitions):
        wb = Workbook()
        ws = wb.active
        ws.title = "conf"
        for family, output_name, classname in definitions:
            for row in [["sl", "string", "string", "string", "string"],
                        [None, "input", "output", "classname", "reward"],
                        [None, "/asset_package/Donor_Package.proto.js",
                         f"/{family}/Event_2026/{output_name}.proto.js", classname,
                         "asset=Donor_Package:1"], []]:
                ws.append(row)
        wb.save(path)
        wb.close()

    def test_collects_all_package_families_manual_classnames_and_no_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            a, b = folder / "resources.xlsx", folder / "interactive.xlsx"
            self.table(a, [("asset_package", "Event_2026_Old_Package", "Event_2026_Manual_Package"),
                           ("quest_item", "Event_2026_PER_1", "Event_2026_PER_1"),
                           ("asset_package", "Event_2026_GR_10_Package", "Event_2026_GR_10_Package")])
            self.table(b, [("asset_package", "Event_2026_Manual_Package", "Event_2026_Manual_Package"),
                           ("asset_package", "Event_2026_GR_2_Package", None),
                           ("asset_package", "Event_2026_GR_1_Money_x01", "Event_2026_GR_1_Money_x01")])
            (folder / "~$locked.xlsx").write_bytes(b"Excel lock")
            snapshots = {p: p.read_bytes() for p in (a, b)}
            result = package_list.build("Event_2026", folder)
            self.assertEqual(result["packages"], 4)
            lines = Path(result["txt"]).read_text(encoding="utf-8").splitlines()
            self.assertEqual(lines[:3], [package_list.SHOP_DIRECTORY, package_list.SHOP_FILE, ""])
            self.assertTrue(all(line.startswith('"') and line.endswith('",') for line in lines[3:]))
            self.assertEqual([json.loads(line[:-1]) for line in lines[3:]],
                             ["Event_2026_GR_1_Money_x01", "Event_2026_GR_2_Package",
                              "Event_2026_GR_10_Package", "Event_2026_Manual_Package"])
            self.assertTrue(all(p.read_bytes() == original for p, original in snapshots.items()))

    def test_repeat_does_not_rewrite_and_new_tables_refresh_the_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            self.table(folder / "a.xlsx", [("asset_package", "Event_2026_ASK_1_Package", None)])
            path = Path(package_list.build("Event_2026", folder)["txt"])
            before = path.stat().st_mtime_ns
            package_list.build("Event_2026", folder)
            self.assertEqual(path.stat().st_mtime_ns, before)
            self.table(folder / "b.xlsx", [("asset_package", "Event_2026_PER_1_Package", None)])
            self.assertEqual(package_list.build("Event_2026", folder)["packages"], 2)
            self.assertIn('"Event_2026_PER_1_Package",', path.read_text(encoding="utf-8"))

    def test_final_conf_writer_always_creates_and_updates_the_sidecar(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for name in ("Event_2026_Chest_GR_1_Package", "Event_2026_FunCollection_4_GR_1_Package"):
                rows = [["sl", "string", "string", "string"],
                        [None, "input", "output", "classname"],
                        [None, "/asset_package/Donor.proto.js", f"/asset_package/{name}.proto.js", name]]
                export_xlsx.write_workbook(folder / (name + ".xlsx"),
                                          [export_xlsx.WorkbookSheet("conf", rows, "interactive")],
                                          campaign_id="Event_2026")
            txt = folder / package_list.filename("Event_2026")
            self.assertEqual(len(txt.read_text(encoding="utf-8").splitlines()[3:]), 2)
            self.assertEqual(len(list(folder.glob("*.txt"))), 2)

    def test_foreign_package_names_and_unresolved_formulas_are_not_silently_copied(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for bad in ("Donor_Package", "=D4"):
                self.table(folder / "a.xlsx", [("asset_package", "Event_2026_GR_1_Package", bad)])
                with self.assertRaisesRegex(ValueError, "invalid or foreign"):
                    package_list.build("Event_2026", folder)
                self.assertFalse((folder / package_list.filename("Event_2026")).exists())

    def test_empty_package_set_still_gets_shop_links_and_missing_tables_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            with self.assertRaisesRegex(ValueError, "No XLSX"):
                package_list.build("Event_2026", folder)
            self.table(folder / "a.xlsx", [("quest_item", "Event_2026_GR_1", None)])
            result = package_list.build("Event_2026", folder)
            self.assertEqual(result["packages"], 0)
            self.assertEqual(Path(result["txt"]).read_text(encoding="utf-8"), package_list.render([]))


if __name__ == "__main__":
    unittest.main()
