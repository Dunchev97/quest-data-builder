from pathlib import Path
import tempfile
import unittest

from openpyxl import load_workbook

from src import converter_tables, export_xlsx, mystery_rewards as mb
from src.technical_quest_tables import collect_cleanup
from src.validate_proto_exports import expected_updates, table_paths


INGREDIENTS = 'asset=Event_2026_ASK_1:17+asset=Event_2026_GR_3:9+asset=Event_2026_Chest_1_R_1:2+asset=Event_2026_Exchanger_R_1:4'


class MysteryRewardsTests(unittest.TestCase):
    def source(self, folder, ingredients=INGREDIENTS, name='resources.xlsx'):
        path = folder / name
        rows = [['sl','string','string','string','string','int'],
                [None,'input','output','identifier','ingredients','id'],
                [None,'/recipe/Donor.proto.js','/recipe/Event_2026/Event_2026_R_1_Recipe.proto.js',
                 'Event_2026_R_1_Recipe',ingredients,None]]
        export_xlsx.write_workbook(path,[export_xlsx.WorkbookSheet('conf',rows,'test')])
        return path

    def test_nine_prototypes_share_the_exact_manual_first_recipe_ingredients(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source = self.source(folder)
            before = source.read_bytes()
            result = mb.build('Event_2026',folder)
            path = Path(result['xlsx'])
            self.assertEqual(path.name,'MB_RECIPEMB_POTS_Event_2026.xlsx')
            self.assertEqual(len(table_paths(path)),9)
            self.assertEqual(converter_tables.validate(path),[])
            updates = expected_updates(path)
            recipes = [(p,f) for p,f,_ in updates if p.startswith('/recipe/')]
            self.assertEqual(len(recipes),3)
            self.assertTrue(all(f['ingredients']==INGREDIENTS for _,f in recipes))
            self.assertTrue(all(f['conditions']=='accomplished_or_restarted_group=Event_2026_Story' for _,f in recipes))
            self.assertEqual(source.read_bytes(),before)
            wb = load_workbook(path,data_only=False)
            self.assertIsNone(wb.active.freeze_panes)
            self.assertFalse(any(c.data_type=='f' for row in wb.active for c in row))
            wb.close()

    def test_manual_titles_ids_and_formulas_survive_addressed_ingredient_update(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source = self.source(folder)
            path = Path(mb.build('Event_2026',folder)['xlsx'])
            w = load_workbook(path)
            w.active['E4']='Мой ручной подарок'
            w.active['G4']='=123+1'
            w.save(path)
            w.close()
            content = path.read_bytes()
            self.assertEqual(mb.ensure('Event_2026',folder),path)
            self.assertEqual(path.read_bytes(),content)
            self.source(folder,INGREDIENTS.replace(':17',':23'))
            with self.assertRaisesRegex(ValueError,'differs from'):
                mb.ensure('Event_2026',folder)
            changed = mb.update_ingredients('Event_2026',folder)
            self.assertEqual(len(changed),3)
            w=load_workbook(path,data_only=False)
            self.assertEqual(w.active['E4'].value,'Мой ручной подарок')
            self.assertEqual(w.active['G4'].value,'=123+1')
            w.close()
            mb.validate_ingredients(path,'Event_2026',[source])
            self.assertEqual(mb.update_ingredients('Event_2026',folder),{})

    def test_missing_or_conflicting_first_recipe_never_creates_a_fake_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            with self.assertRaisesRegex(ValueError,'unambiguous'):
                mb.build('Event_2026',folder)
            self.source(folder)
            self.source(folder,INGREDIENTS+':different',name='other.xlsx')
            with self.assertRaisesRegex(ValueError,'unambiguous'):
                mb.build('Event_2026',folder)
            self.assertFalse((folder/mb.filename('Event_2026')).exists())

    def test_rule_also_applies_to_any_additional_manually_added_mb_recipe(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            self.source(folder)
            path=Path(mb.build('Event_2026',folder)['xlsx'])
            w=load_workbook(path)
            for row in [[],['sl','string','string','string','string'],
                        [None,'input','output','identifier','ingredients'],
                        [None,'/recipe/Donor.proto.js','/recipe/Event_2026/Event_2026_R_MB_4_Recipe.proto.js',
                         'Event_2026_R_MB_4_Recipe','asset=Wrong:1']]:
                w.active.append(row)
            w.save(path)
            w.close()
            with self.assertRaisesRegex(ValueError,'R_MB_4'):
                mb.validate_ingredients(path,'Event_2026',folder.glob('*.xlsx'))
            self.assertEqual(len(mb.update_ingredients('Event_2026',folder)),1)
            mb.validate_ingredients(path,'Event_2026',folder.glob('*.xlsx'))

    def test_cleanup_removes_event_boxes_but_preserves_prize_pots(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            source=self.source(folder)
            path=Path(mb.build('Event_2026',folder)['xlsx'])
            actions,summary=collect_cleanup('Event_2026',[source,path])
            removed={a['classname'] for a in actions if a['do']=='remove_asset'}
            self.assertEqual(removed,{f'Event_2026_R_MB_{n}' for n in (1,2,3)})
            self.assertFalse(any('_Pot_' in str(a) for a in actions))
            self.assertEqual(summary['assets'],3)


if __name__=='__main__':
    unittest.main()
