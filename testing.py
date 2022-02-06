import unittest
import os
from tareas import *

class TestExcercise(unittest.TestCase):
    
    def test_encrypt(self):
        self.assertEqual(Tareas().encriptar_sha1('12345'), '8cb2237d0679ca88db6464eac60da96345513964')

    def test_generated_database_file(self):
        fileNameDb = "generate/dataframe_test.db"
        self.assertTrue(os.path.isfile(fileNameDb))

    def test_generated_json_file(self):
        fileNameJson = "generate/df_to_json.json"
        self.assertTrue(os.path.isfile(fileNameJson))        

if __name__ == '__main__':
    tarea = Tareas()
    countries = tarea.countries_service()
    df_filled=tarea.fill_dataframe(c=countries)
    tarea.store_db(df_filled)
    tarea.dataframe_to_json(df_filled)
    tarea.show_data(df_filled)
    unittest.main()