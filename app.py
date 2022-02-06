if __name__ == '__main__':
    from tareas import Tareas
    tarea = Tareas()
    countries = tarea.countries_service()
    df_filled=tarea.fill_dataframe(c=countries)
    tarea.store_db(df_filled)
    tarea.dataframe_to_json(df_filled)
    tarea.show_data(df_filled)