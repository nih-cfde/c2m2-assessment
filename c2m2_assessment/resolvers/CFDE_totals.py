from c2m2_assessment.util.memo import memo

total_files = memo(lambda CFDE: CFDE.tables['file'].count())
total_collections = memo(lambda CFDE: CFDE.tables['collection'].count())
total_biosamples = memo(lambda CFDE: CFDE.tables['biosample'].count())
total_subjects = memo(lambda CFDE: CFDE.tables['subject'].count())
total_projects = memo(lambda CFDE: CFDE.tables['project'].count())
# entity_counts = memo(lambda CFDE: pd.Series({
#   name: table.count()
#   for name, table in CFDE.tables.items()
# }).to_frame('Entity Counts'))
