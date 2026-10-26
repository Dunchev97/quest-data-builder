import tempfile
import unittest
from pathlib import Path

from openpyxl import load_workbook

from src.build_filled_tasks import BuildState
from src.export_xlsx import WorkbookSheet, write_workbook
from src.quest_naming import normalize_character_references, normalize_generated_reference


class QuestNamingTests(unittest.TestCase):
    def test_emotion_defaults_to_one_and_keeps_explicit_emotions(self):
        self.assertEqual(normalize_character_references('Event_2026_Character_12','Event_2026'),'Event_2026_Character_12_1')
        self.assertEqual(normalize_character_references('Event_2026_Character_12_4','Event_2026'),'Event_2026_Character_12_4')
        self.assertEqual(normalize_character_references('Event_2026_Character_12_Dialog_3','Event_2026'),'Event_2026_Character_12_1_Dialog_3')
        self.assertEqual(normalize_character_references('Fun13_Character_12','Event_2026'),'Fun13_Character_12')

    def test_go_to_location_json_keeps_the_same_character_reference(self):
        before='[{"classname":"Event_2026_Character_3"}]'
        self.assertEqual(normalize_character_references(before,'Event_2026'),'[{"classname":"Event_2026_Character_3_1"}]')

    def test_outputs_use_campaign_directly_for_furniture_and_actions(self):
        self.assertEqual(normalize_generated_reference('/furniture/Fun/Event_2026/Character/Event_2026_Character_2.proto.js','Event_2026'),'/furniture/Event_2026/Character/Event_2026_Character_2_1.proto.js')
        self.assertEqual(normalize_generated_reference('/quest_action/Fun/Event_2026/search_Event_2026_HOG_1.proto.js','Event_2026'),'/quest_action/Event_2026/search_Event_2026_HOG_1.proto.js')

    def test_give_uses_character_number_instead_of_emotion_number(self):
        state=BuildState({})
        self.assertEqual(state.character_classname('Event_2026','Cat'),'Event_2026_Character_1_1')
        self.assertEqual(state.character_classname('Event_2026','Cat','Event_2026_Character_3'),'Event_2026_Character_3_1')
        self.assertEqual(state.next_give_classname('Event_2026','Event_2026_Character_3_4'),'Event_2026_Give_3_1')

    def test_every_table_source_clears_ids_including_supplied_reference_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            for source in ['generated_quests','generated_actions','resource_table','interactive:chest_1','fun:FunCollection_4','quest_accomplished']:
                rows=[['sl','string','string','string','int'],['','input','output','classname','id'],
                      ['','/furniture/Fun/Fun13/Character/Fun13_Character_23.proto.js','/furniture/Fun/Event_2026/Character/Event_2026_Character_1.proto.js','Event_2026_Character_1',125015]]
                path=Path(tmp)/(source.replace(':','_')+'.xlsx')
                write_workbook(path,[WorkbookSheet('conf',rows,source)],campaign_id='Event_2026')
                book=load_workbook(path)
                self.assertIsNone(book.active['E3'].value)
                self.assertEqual(book.active['D3'].value,'Event_2026_Character_1_1')
                self.assertEqual(book.active['C3'].value,'/furniture/Event_2026/Character/Event_2026_Character_1_1.proto.js')
                self.assertEqual(book.active['B3'].value,'/furniture/Fun/Fun13/Character/Fun13_Character_23.proto.js')
                book.close()


if __name__=='__main__':
    unittest.main()
