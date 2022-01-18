#%%
import re
import click
import pandas as pd
import logging
from c2m2_assessment.util.one import one
from c2m2_assessment.util.memo import memo
from c2m2_assessment.util.fetch_cache import fetch_cache
from c2m2_assessment.util.rubric import Rubric

logger = logging.getLogger(__name__)

#%%
rubric = Rubric()

#%%
total_files = memo(lambda CFDE: CFDE.tables['file'].count())
total_collections = memo(lambda CFDE: CFDE.tables['collection'].count())
total_biosamples = memo(lambda CFDE: CFDE.tables['biosample'].count())
total_subjects = memo(lambda CFDE: CFDE.tables['subject'].count())
total_projects = memo(lambda CFDE: CFDE.tables['project'].count())
# entity_counts = memo(lambda CFDE: pd.Series({
#   name: table.count()
#   for name, table in CFDE.tables.items()
# }).to_frame('Entity Counts'))

#%%
@rubric.metric({
  # standardized metadata format (107), machine readable metadata (106)
  # metadata license (117) (c2m2 ?)
  '@id': 106,
  'name': 'Metadata conformance',
  'description': 'The metadata properly conforms with the CFDE perscribed metadata model specification',
  'detail': '''The average metadata coverage of all tables''',
  'principle': 'Findable',
})
def _(CFDE, full=False, **kwargs):
  def count_empty(val):
    ''' Attempt to catch some actual null values that aren't really null.
    '''
    return sum(
      1
      for v in val
      if v is not None and (
        type(v) != str or v.strip().lower() not in {
          '-', '-666', '', 'empty', 'n/a', 'na',
          'nan', 'nil', 'none', 'not defined', 'null',
          'undef', 'undefined',
        }
      )
    )
  coverage = pd.DataFrame(
    dict(
      table=table_name,
      coverage=count_empty(entity.values()) / len(table.column_definitions.keys()),
    )
    for table_name, table in CFDE.tables.items()
    for entity in table.entities()
  ).groupby('table')['coverage'].describe().fillna(0).sort_values('mean')
  value = coverage['mean'].mean()
  return {
    'value': value,
    'comment': f'See metadata coverage for more info',
    'supplement': coverage.to_dict(),
  }

#%%
@rubric.metric({
  # Persistent identifier (105)
  '@id': 104,
  'name': 'Persistent identifier',
  'description': 'Globally unique, persistent, and valid identifiers (preferrably DOIs) are present for the dataset',
  'detail': '''We check that the persistent id that are present''',
  'principle': 'Findable',
})
def _(CFDE, full=False, **kwargs):
  qualified_persistent_ids = pd.Series({
    (file['id_namespace'], file['local_id'], file.get('persistent_id')): 1 if file.get('persistent_id') else 0
    for file in CFDE.tables['file'].entities()
  }).sort_values()
  total_qualified_persistent_ids = qualified_persistent_ids.sum()
  value = (total_qualified_persistent_ids / total_files(CFDE)) if total_files(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f'{total_qualified_persistent_ids} / {total_files(CFDE)}',
    'supplement': qualified_persistent_ids.to_dict() if full else pd.concat([
      qualified_persistent_ids.head(5),
      qualified_persistent_ids.tail(5),
    ]).to_dict(),
  }

#%%
@rubric.metric({
  '@id': -1,
  'name': 'ratio files are associated with data type term',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_files_associated_with_data_type = CFDE.tables['data_type'] \
    .link(CFDE.tables['file'], on=(
      CFDE.tables['file'].data_type == CFDE.tables['data_type'].id
    )) \
    .groupby(CFDE.tables['file'].id_namespace, CFDE.tables['file'].local_id) \
    .count()
  value = (total_files_associated_with_data_type / total_files(CFDE)) if total_files(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_files_associated_with_data_type} / {total_files(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -2,
  'name': 'ratio files are associated with file format term',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_files_associated_with_file_format = CFDE.tables['file_format'] \
    .link(CFDE.tables['file'], on=(
      CFDE.tables['file'].file_format == CFDE.tables['file_format'].id
    )) \
    .groupby(CFDE.tables['file'].id_namespace, CFDE.tables['file'].local_id) \
    .count()
  value = (total_files_associated_with_file_format / total_files(CFDE)) if total_files(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_files_associated_with_file_format} / {total_files(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -3,
  'name': 'ratio files are associated with assaytype term',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_files_associated_with_assay_type = CFDE.tables['assay_type'] \
    .link(CFDE.tables['file'], on=(
      CFDE.tables['file'].assay_type == CFDE.tables['assay_type'].id
    )) \
    .groupby(CFDE.tables['file'].id_namespace, CFDE.tables['file'].local_id) \
    .count()
  value = (total_files_associated_with_assay_type / total_files(CFDE)) if total_files(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_files_associated_with_assay_type} / {total_files(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -4,
  'name': 'ratio files are associate with anatomy term',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_files_associated_with_anatomy = CFDE.tables['anatomy'] \
    .link(CFDE.tables['biosample'], on=(
      CFDE.tables['biosample'].anatomy == CFDE.tables['anatomy'].id
    )) \
    .link(CFDE.tables['file_describes_biosample'], on=((
      CFDE.tables['file_describes_biosample'].biosample_id_namespace == CFDE.tables['biosample'].id_namespace
    ) & (
      CFDE.tables['file_describes_biosample'].biosample_local_id == CFDE.tables['biosample'].local_id
    ))) \
    .link(CFDE.tables['file'], on=((
      CFDE.tables['file'].id_namespace == CFDE.tables['file_describes_biosample'].file_id_namespace
    ) & (
      CFDE.tables['file'].local_id == CFDE.tables['file_describes_biosample'].file_local_id
    ))) \
    .groupby(CFDE.tables['file'].id_namespace, CFDE.tables['file'].local_id) \
    .count()
  value = (total_files_associated_with_anatomy / total_files(CFDE)) if total_files(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_files_associated_with_anatomy} / {total_files(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -5,
  'name': 'ratio files are associated with a biosample',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_files_associated_with_biosample = CFDE.tables['biosample'] \
    .link(CFDE.tables['file_describes_biosample'], on=((
      CFDE.tables['file_describes_biosample'].biosample_id_namespace == CFDE.tables['biosample'].id_namespace
    ) & (
      CFDE.tables['file_describes_biosample'].biosample_local_id == CFDE.tables['biosample'].local_id
    ))) \
    .link(CFDE.tables['file'], on=((
      CFDE.tables['file'].id_namespace == CFDE.tables['file_describes_biosample'].file_id_namespace
    ) & (
      CFDE.tables['file'].local_id == CFDE.tables['file_describes_biosample'].file_local_id
    ))) \
    .groupby(CFDE.tables['file'].id_namespace, CFDE.tables['file'].local_id) \
    .count()
  value = (total_files_associated_with_biosample / total_files(CFDE)) if total_files(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_files_associated_with_biosample} / {total_files(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -6,
  'name': 'ratio files are associated with a subject',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_files_associated_with_subject = CFDE.tables['subject'] \
    .link(CFDE.tables['file_describes_subject'], on=((
      CFDE.tables['file_describes_subject'].subject_id_namespace == CFDE.tables['subject'].id_namespace
    ) & (
      CFDE.tables['file_describes_subject'].subject_local_id == CFDE.tables['subject'].local_id
    ))) \
    .link(CFDE.tables['file'], on=((
      CFDE.tables['file'].id_namespace == CFDE.tables['file_describes_subject'].file_id_namespace
    ) & (
      CFDE.tables['file'].local_id == CFDE.tables['file_describes_subject'].file_local_id
    ))) \
    .groupby(CFDE.tables['file'].id_namespace, CFDE.tables['file'].local_id) \
    .count()
  value = (total_files_associated_with_subject / total_files(CFDE)) if total_files(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_files_associated_with_subject} / {total_files(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -7,
  'name': 'ratio files are associated with a subject_role_taxonomy',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_files_associated_with_subject_role = CFDE.tables['subject_role_taxonomy'] \
    .link(CFDE.tables['subject'], on=((
      CFDE.tables['subject'].id_namespace == CFDE.tables['subject_role_taxonomy'].subject_id_namespace
    ) & (
      CFDE.tables['subject'].local_id == CFDE.tables['subject_role_taxonomy'].subject_local_id
    ))) \
    .link(CFDE.tables['file_describes_subject'], on=((
      CFDE.tables['file_describes_subject'].subject_id_namespace == CFDE.tables['subject'].id_namespace
    ) & (
      CFDE.tables['file_describes_subject'].subject_local_id == CFDE.tables['subject'].local_id
    ))) \
    .link(CFDE.tables['file'], on=((
      CFDE.tables['file'].id_namespace == CFDE.tables['file_describes_subject'].file_id_namespace
    ) & (
      CFDE.tables['file'].local_id == CFDE.tables['file_describes_subject'].file_local_id
    ))) \
    .groupby(CFDE.tables['file'].id_namespace, CFDE.tables['file'].local_id) \
    .count()
  value = (total_files_associated_with_subject_role / total_files(CFDE)) if total_files(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_files_associated_with_subject_role} / {total_files(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -8,
  'name': 'ratio biosamples are associated with a species term (NCBI Taxon)',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_biosamples_associated_with_ncbi_taxon = CFDE.tables['ncbi_taxonomy'] \
    .link(CFDE.tables['subject_role_taxonomy'], on=(
      CFDE.tables['subject_role_taxonomy'].taxonomy_id == CFDE.tables['ncbi_taxonomy'].id
    )) \
    .link(CFDE.tables['subject'], on=((
      CFDE.tables['subject'].id_namespace == CFDE.tables['subject_role_taxonomy'].subject_id_namespace
    ) & (
      CFDE.tables['subject'].local_id == CFDE.tables['subject_role_taxonomy'].subject_local_id
    ))) \
    .link(CFDE.tables['biosample_from_subject'], on=((
      CFDE.tables['biosample_from_subject'].subject_id_namespace == CFDE.tables['subject'].id_namespace
    ) & (
      CFDE.tables['biosample_from_subject'].subject_local_id == CFDE.tables['subject'].local_id
    ))) \
    .link(CFDE.tables['biosample'], on=((
      CFDE.tables['biosample'].id_namespace == CFDE.tables['biosample_from_subject'].biosample_id_namespace
    ) & (
      CFDE.tables['biosample'].local_id == CFDE.tables['biosample_from_subject'].biosample_local_id
    ))) \
    .groupby(CFDE.tables['biosample'].id_namespace, CFDE.tables['biosample'].local_id) \
    .count()
  value = (total_biosamples_associated_with_ncbi_taxon / total_biosamples(CFDE)) if total_biosamples(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_biosamples_associated_with_ncbi_taxon} / {total_biosamples(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -9,
  'name': 'ratio biosamples are associated with a subject',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_biosamples_associated_with_subject = CFDE.tables['subject'] \
    .link(CFDE.tables['biosample_from_subject'], on=((
      CFDE.tables['biosample_from_subject'].subject_id_namespace == CFDE.tables['subject'].id_namespace
    ) & (
      CFDE.tables['biosample_from_subject'].subject_local_id == CFDE.tables['subject'].local_id
    ))) \
    .link(CFDE.tables['biosample'], on=((
      CFDE.tables['biosample'].id_namespace == CFDE.tables['biosample_from_subject'].biosample_id_namespace
    ) & (
      CFDE.tables['biosample'].local_id == CFDE.tables['biosample_from_subject'].biosample_local_id
    ))) \
    .groupby(CFDE.tables['biosample'].id_namespace, CFDE.tables['biosample'].local_id) \
    .count()
  value = (total_biosamples_associated_with_subject / total_biosamples(CFDE)) if total_biosamples(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_biosamples_associated_with_subject} / {total_biosamples(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -10,
  'name': 'ratio biosamples are associated with a file',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_biosamples_associated_with_file = CFDE.tables['file'] \
    .link(CFDE.tables['file_describes_biosample'], on=((
      CFDE.tables['file_describes_biosample'].file_id_namespace == CFDE.tables['file'].id_namespace
    ) & (
      CFDE.tables['file_describes_biosample'].file_local_id == CFDE.tables['file'].local_id
    ))) \
    .link(CFDE.tables['biosample'], on=((
      CFDE.tables['biosample'].id_namespace == CFDE.tables['file_describes_biosample'].biosample_id_namespace
    ) & (
      CFDE.tables['biosample'].local_id == CFDE.tables['file_describes_biosample'].biosample_local_id
    ))) \
    .groupby(CFDE.tables['biosample'].id_namespace, CFDE.tables['biosample'].local_id) \
    .count()
  value = (total_biosamples_associated_with_file / total_biosamples(CFDE)) if total_biosamples(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_biosamples_associated_with_file} / {total_biosamples(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -11,
  'name': 'ratio biosamples are associated with an anatomy term',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_biosamples_associated_with_anatomy = CFDE.tables['anatomy'] \
    .link(CFDE.tables['biosample'], on=(
      CFDE.tables['biosample'].anatomy == CFDE.tables['anatomy'].id
    )) \
    .groupby(CFDE.tables['biosample'].id_namespace, CFDE.tables['biosample'].local_id) \
    .count()
  value = (total_biosamples_associated_with_anatomy / total_biosamples(CFDE)) if total_biosamples(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_biosamples_associated_with_anatomy} / {total_biosamples(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -12,
  'name': 'ratio biosamples are associated with an assay term',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_biosamples_associated_with_assay = CFDE.tables['file'].filter(CFDE.tables['file'].assay_type != None)   .link(CFDE.tables['file_describes_biosample'], on=((
      CFDE.tables['file_describes_biosample'].file_id_namespace == CFDE.tables['file'].id_namespace
    ) & (
      CFDE.tables['file_describes_biosample'].file_local_id == CFDE.tables['file'].local_id
    ))) \
    .link(CFDE.tables['biosample'], on=((
      CFDE.tables['biosample'].id_namespace == CFDE.tables['file_describes_biosample'].biosample_id_namespace
    ) & (
      CFDE.tables['biosample'].local_id == CFDE.tables['file_describes_biosample'].biosample_local_id
    ))) \
    .groupby(CFDE.tables['biosample'].id_namespace, CFDE.tables['biosample'].local_id) \
    .count()
  value = (total_biosamples_associated_with_assay / total_biosamples(CFDE)) if total_biosamples(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_biosamples_associated_with_assay} / {total_biosamples(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -13,
  'name': 'ratio subjects are associated with a taxonomy',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_subjects_associated_with_taxonomy = CFDE.tables['ncbi_taxonomy'] \
    .link(CFDE.tables['subject_role_taxonomy'], on=(
      CFDE.tables['subject_role_taxonomy'].taxonomy_id == CFDE.tables['ncbi_taxonomy'].id
    )) \
    .link(CFDE.tables['subject'], on=((
      CFDE.tables['subject'].id_namespace == CFDE.tables['subject_role_taxonomy'].subject_id_namespace
    ) & (
      CFDE.tables['subject'].local_id == CFDE.tables['subject_role_taxonomy'].subject_local_id
    ))) \
    .groupby(CFDE.tables['subject'].id_namespace, CFDE.tables['subject'].local_id) \
    .count()
  value = (total_subjects_associated_with_taxonomy / total_subjects(CFDE)) if total_subjects(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_subjects_associated_with_taxonomy} / {total_subjects(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -14,
  'name': 'ratio subjects have subject granularity',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_subjects_associated_with_granularity = CFDE.tables['subject'].filter(
    (CFDE.tables['subject'].granularity != None) & (CFDE.tables['subject'].granularity != '')
  ).count()
  value = (total_subjects_associated_with_granularity / total_subjects(CFDE)) if total_subjects(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_subjects_associated_with_granularity} / {total_subjects(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -15,
  'name': 'ratio subjects have taxonomic role',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_subjects_associated_with_role_taxonomy = CFDE.tables['subject_role_taxonomy'] \
    .link(CFDE.tables['subject'], on=((
      CFDE.tables['subject'].id_namespace == CFDE.tables['subject_role_taxonomy'].subject_id_namespace
    ) & (
      CFDE.tables['subject'].local_id == CFDE.tables['subject_role_taxonomy'].subject_local_id
    ))) \
    .groupby(CFDE.tables['subject'].id_namespace, CFDE.tables['subject'].local_id) \
    .count()
  value = (total_subjects_associated_with_role_taxonomy / total_subjects(CFDE)) if total_subjects(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_subjects_associated_with_role_taxonomy} / {total_subjects(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -16,
  'name': 'ratio subjects associated with a biosample',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_subjects_associated_with_biosample = CFDE.tables['biosample'] \
    .link(CFDE.tables['biosample_from_subject'], on=((
      CFDE.tables['biosample_from_subject'].biosample_id_namespace == CFDE.tables['biosample'].id_namespace
    ) & (
      CFDE.tables['biosample_from_subject'].biosample_local_id == CFDE.tables['biosample'].local_id
    ))) \
    .link(CFDE.tables['subject'], on=((
      CFDE.tables['subject'].id_namespace == CFDE.tables['biosample_from_subject'].subject_id_namespace
    ) & (
      CFDE.tables['subject'].local_id == CFDE.tables['biosample_from_subject'].subject_local_id
    ))) \
    .groupby(CFDE.tables['subject'].id_namespace, CFDE.tables['subject'].local_id) \
    .count()
  value = (total_subjects_associated_with_biosample / total_subjects(CFDE)) if total_subjects(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_subjects_associated_with_biosample} / {total_subjects(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -17,
  'name': 'ratio subjects associated with a file',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_subjects_associated_with_file = CFDE.tables['file'] \
    .link(CFDE.tables['file_describes_subject'], on=((
      CFDE.tables['file_describes_subject'].file_id_namespace == CFDE.tables['file'].id_namespace
    ) & (
      CFDE.tables['file_describes_subject'].file_local_id == CFDE.tables['file'].local_id
    ))) \
    .link(CFDE.tables['subject'], on=((
      CFDE.tables['subject'].id_namespace == CFDE.tables['file_describes_subject'].subject_id_namespace
    ) & (
      CFDE.tables['subject'].local_id == CFDE.tables['file_describes_subject'].subject_local_id
    ))) \
    .groupby(CFDE.tables['subject'].id_namespace, CFDE.tables['subject'].local_id) \
    .count()
  value = (total_subjects_associated_with_file / total_subjects(CFDE)) if total_subjects(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_subjects_associated_with_file} / {total_subjects(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -18,
  'name': 'IF there are collections: # of files that are part of a collection',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_files_not_in_collection = CFDE.tables['collection'] \
    .link(CFDE.tables['file_in_collection'], on=((
      CFDE.tables['file_in_collection'].collection_id_namespace == CFDE.tables['collection'].id_namespace
    ) & (
      CFDE.tables['file_in_collection'].collection_local_id == CFDE.tables['collection'].local_id
    ))) \
    .link(CFDE.tables['file'], on=((
      CFDE.tables['file'].id_namespace == CFDE.tables['file_in_collection'].file_id_namespace
    ) & (
      CFDE.tables['file'].local_id == CFDE.tables['file_in_collection'].file_local_id
    ))) \
    .groupby(CFDE.tables['file'].id_namespace, CFDE.tables['file'].local_id) \
    .count()
  value = (total_files_not_in_collection / total_files(CFDE)) if total_files(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_files_not_in_collection} / {total_files(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -19,
  'name': 'IF there are collections: # of subjects that are part of a collection',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_subjects_not_in_collection = CFDE.tables['collection'] \
    .link(CFDE.tables['subject_in_collection'], on=((
      CFDE.tables['subject_in_collection'].collection_id_namespace == CFDE.tables['collection'].id_namespace
    ) & (
      CFDE.tables['subject_in_collection'].collection_local_id == CFDE.tables['collection'].local_id
    ))) \
    .link(CFDE.tables['subject'], on=((
      CFDE.tables['subject'].id_namespace == CFDE.tables['subject_in_collection'].subject_id_namespace
    ) & (
      CFDE.tables['subject'].local_id == CFDE.tables['subject_in_collection'].subject_local_id
    ))) \
    .groupby(CFDE.tables['subject'].id_namespace, CFDE.tables['subject'].local_id) \
    .count()
  value = (total_subjects_not_in_collection / total_subjects(CFDE)) if total_subjects(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_subjects_not_in_collection} / {total_subjects(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -20,
  'name': 'IF there are collections: # of biosamples that are part of a collection',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_biosamples_not_in_collection = CFDE.tables['collection'] \
    .link(CFDE.tables['biosample_in_collection'], on=((
      CFDE.tables['biosample_in_collection'].collection_id_namespace == CFDE.tables['collection'].id_namespace
    ) & (
      CFDE.tables['biosample_in_collection'].collection_local_id == CFDE.tables['collection'].local_id
    ))) \
    .link(CFDE.tables['biosample'], on=((
      CFDE.tables['biosample'].id_namespace == CFDE.tables['biosample_in_collection'].biosample_id_namespace
    ) & (
      CFDE.tables['biosample'].local_id == CFDE.tables['biosample_in_collection'].biosample_local_id
    ))) \
    .groupby(CFDE.tables['biosample'].id_namespace, CFDE.tables['biosample'].local_id) \
    .count()
  value = (total_biosamples_not_in_collection / total_biosamples(CFDE)) if total_biosamples(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_biosamples_not_in_collection} / {total_biosamples(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -21,
  'name': 'Project associated with anatomy',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  # NOTE: does not include recursive projects
  total_projects_associated_with_anatomy = CFDE.tables['anatomy'] \
    .link(CFDE.tables['biosample'], on=(
      CFDE.tables['biosample'].anatomy == CFDE.tables['anatomy'].id
    )) \
    .link(CFDE.tables['project'], on=((
      CFDE.tables['project'].id_namespace == CFDE.tables['biosample'].project_id_namespace
    ) & (
      CFDE.tables['project'].local_id == CFDE.tables['biosample'].project_local_id
    ))) \
    .groupby(CFDE.tables['project'].id_namespace, CFDE.tables['project'].local_id) \
    .count()
  value = (total_projects_associated_with_anatomy / total_projects(CFDE)) if total_projects(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_projects_associated_with_anatomy} / {total_projects(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -22,
  'name': 'Project associated with files',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  # NOTE: does not include recursive projects
  total_projects_associated_with_file = CFDE.tables['file'] \
    .link(CFDE.tables['project'], on=((
      CFDE.tables['project'].id_namespace == CFDE.tables['file'].project_id_namespace
    ) & (
      CFDE.tables['project'].local_id == CFDE.tables['file'].project_local_id
    ))) \
    .groupby(CFDE.tables['project'].id_namespace, CFDE.tables['project'].local_id) \
    .count()
  value = (total_projects_associated_with_file / total_projects(CFDE)) if total_projects(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_projects_associated_with_file} / {total_projects(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -23,
  'name': 'Project associated with data types',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  # NOTE: does not include recursive projects
  total_projects_associated_with_data_type = CFDE.tables['data_type'] \
    .link(CFDE.tables['file'], on=(
      CFDE.tables['file'].data_type == CFDE.tables['data_type'].id
    )) \
    .link(CFDE.tables['project'], on=((
      CFDE.tables['project'].id_namespace == CFDE.tables['file'].project_id_namespace
    ) & (
      CFDE.tables['project'].local_id == CFDE.tables['file'].project_local_id
    ))) \
    .groupby(CFDE.tables['project'].id_namespace, CFDE.tables['project'].local_id) \
    .count()
  value = (total_projects_associated_with_data_type / total_projects(CFDE)) if total_projects(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_projects_associated_with_data_type} / {total_projects(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -24,
  'name': 'Project associated with subjects',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  # NOTE: does not include recursive projects
  total_projects_associated_with_subject = CFDE.tables['subject'] \
    .link(CFDE.tables['project'], on=((
      CFDE.tables['project'].id_namespace == CFDE.tables['subject'].project_id_namespace
    ) & (
      CFDE.tables['project'].local_id == CFDE.tables['subject'].project_local_id
    ))) \
    .groupby(CFDE.tables['project'].id_namespace, CFDE.tables['project'].local_id) \
    .count()
  value = (total_projects_associated_with_subject / total_projects(CFDE)) if total_projects(CFDE) else float('nan')
  return {
    'value': value,
    'comment': f"{total_projects_associated_with_subject} / {total_projects(CFDE)}",
  }

#%%
@rubric.metric({
  '@id': -25,
  'name': 'list of any anatomy terms in anatomy.tsv NOT associated with biosamples',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  # TODO: we can probably use an outer join for this..
  used_anatomy_terms = CFDE.tables['biosample'] \
      .link(CFDE.tables['anatomy'], on=(
          CFDE.tables['anatomy'].id == CFDE.tables['biosample'].anatomy
      )) \
      .groupby(CFDE.tables['anatomy'].id)
  used_anatomy_ids = {
      anatomy['id']
      for anatomy in used_anatomy_terms.entities()
  }
  unused_anatomy_terms = pd.DataFrame({
      anatomy['id']: anatomy
      for anatomy in CFDE.tables['anatomy'].entities()
      if anatomy['id'] not in used_anatomy_ids
  }).T
  total = len(used_anatomy_ids) + unused_anatomy_terms.shape[0]
  value = (1 - (unused_anatomy_terms.shape[0] / total)) if total else float('nan')
  return {
    'value': value,
    'comment': f"{len(used_anatomy_ids)} / {total}",
    'supplement': unused_anatomy_terms.to_dict(),
  }

#%%
@rubric.metric({
  '@id': -26,
  'name': 'list of any species terms in ncbi_taxonomy.tsv NOT associated with a subject',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  # TODO: we can probably use an outer join for this..
  used_taxonomy_terms = CFDE.tables['subject'] \
      .link(CFDE.tables['subject_role_taxonomy'], on=((
          CFDE.tables['subject_role_taxonomy'].subject_id_namespace == CFDE.tables['subject'].id_namespace
      ) & (
          CFDE.tables['subject_role_taxonomy'].subject_local_id == CFDE.tables['subject'].local_id
      ))) \
      .link(CFDE.tables['ncbi_taxonomy'], on=(
          CFDE.tables['ncbi_taxonomy'].id == CFDE.tables['subject_role_taxonomy'].taxonomy_id
      )) \
      .groupby(CFDE.tables['ncbi_taxonomy'].id)
  used_taxonomy_ids = {
      taxonomy['id']
      for taxonomy in used_taxonomy_terms.entities()
  }
  unused_taxonomy_terms = pd.DataFrame({
      taxonomy['id']: taxonomy
      for taxonomy in CFDE.tables['ncbi_taxonomy'].entities()
      if taxonomy['id'] not in used_taxonomy_ids
  }).T
  total = len(used_taxonomy_ids) + unused_taxonomy_terms.shape[0]
  value = (1 - (unused_taxonomy_terms.shape[0] / total)) if total else float('nan')
  return {
    'value': value,
    'comment': f"{len(used_taxonomy_ids)} / {total}",
    'supplement': unused_taxonomy_terms.to_dict(),
  }

#%%
@rubric.metric({
  '@id': -27,
  'name': 'list of any assay terms in assay_type.tsv NOT associated with files',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  used_assay_type_terms = CFDE.tables['file'] \
      .link(CFDE.tables['assay_type'], on=(
          CFDE.tables['assay_type'].id == CFDE.tables['file'].assay_type
      )) \
      .groupby(CFDE.tables['assay_type'].id)
  used_assay_type_ids = {
      assay_type['id']
      for assay_type in used_assay_type_terms.entities()
  }
  unused_assay_type_terms = pd.DataFrame({
      assay_type['id']: assay_type
      for assay_type in CFDE.tables['assay_type'].entities()
      if assay_type['id'] not in used_assay_type_ids
  }).T
  total = len(used_assay_type_ids) + unused_assay_type_terms.shape[0]
  value = (1 - (unused_assay_type_terms.shape[0] / total)) if total else float('nan')
  return {
    'value': value,
    'comment': f"{len(used_assay_type_ids)} / {total}",
    'supplement': unused_assay_type_terms.to_dict(),
  }

#%%
@rubric.metric({
  '@id': -28,
  'name': 'list of any format terms in file_format.tsv NOT associated with files',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  used_file_format_terms = CFDE.tables['file'] \
      .link(CFDE.tables['file_format'], on=(
          CFDE.tables['file_format'].id == CFDE.tables['file'].file_format
      )) \
      .groupby(CFDE.tables['file_format'].id)
  used_file_format_ids = {
      file_format['id']
      for file_format in used_file_format_terms.entities()
  }
  unused_file_format_terms = pd.DataFrame({
      file_format['id']: file_format
      for file_format in CFDE.tables['file_format'].entities()
      if file_format['id'] not in used_file_format_ids
  }).T
  total = len(used_file_format_ids) + unused_file_format_terms.shape[0]
  value = (1 - (unused_file_format_terms.shape[0] / total)) if total else float('nan')
  return {
    'value': value,
    'comment': f"{len(used_file_format_ids)} / {total}",
    'supplement': unused_file_format_terms.to_dict(),
  }

#%%
@rubric.metric({
  '@id': -29,
  'name': 'list of any data type terms in data_type.tsv NOT associated with files',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  used_data_type_terms = CFDE.tables['file'] \
      .link(CFDE.tables['data_type'], on=(
          CFDE.tables['data_type'].id == CFDE.tables['file'].data_type
      )) \
      .groupby(CFDE.tables['data_type'].id)
  used_data_type_ids = {
      data_type['id']
      for data_type in used_data_type_terms.entities()
  }
  unused_data_type_terms = pd.DataFrame({
      data_type['id']: data_type
      for data_type in CFDE.tables['data_type'].entities()
      if data_type['id'] not in used_data_type_ids
  }).T
  total = len(used_data_type_ids) + unused_data_type_terms.shape[0]
  value = (1 - (unused_data_type_terms.shape[0] / total)) if total else float('nan')
  return {
    'value': value,
    'comment': f"{len(used_data_type_ids)} / {total}",
    'supplement': unused_data_type_terms.to_dict(),
  }

#%%
@rubric.metric({
  '@id': 145,
  'name': 'Landing Page',
  'description': 'A landing page exists and is accessible for the identifiers',
  'detail': '''Checks to make sure the persistent_id is resolvable with a HEAD request. if it is not http/https it is assumed to be an identifiers.org-resolvable CURIE. note that this is still error prone, some identifier websites do not follow HTTP standards and may not report 404s with ids that aren't found.''',
  'principle': 'Findable',
  'extended': True,
})
def _(CFDE, full=False, **kwargs):
  return {
    'value': float('nan'),
    'comment': 'Skipped',
  }
  # import requests
  # results = {}
  # for file in CFDE.tables['file'].entities():
  #   file_id = (file['id_namespace'], file['local_id'])
  #   results[file_id] = {}
  #   persistent_id = file.get('persistent_id')
  #   if not persistent_id:
  #     results[file_id]['value'] = 0
  #     results[file_id]['comment'] = "No persistent id present"
  #     continue
  #   if not re.match(r'^https?://', persistent_id):
  #     persistent_id = 'https://identifiers.org/{}'.format(persistent_id)
  #   try:
  #     status_code = requests.head(persistent_id, headers={'User-Agent': None}).status_code
  #     results[file_id]['comment'] = f"Status Code: {status_code}"
  #     if status_code >= 200 and status_code < 300:
  #       results[file_id]['value'] = 1.0
  #     elif status_code >= 300 and status_code < 399:
  #       results[file_id]['value'] = 0.5
  #     elif status_code >= 400:
  #       results[file_id]['value'] = 0.25
  #   except Exception as e:
  #     results[file_id]['value'] = 0.0
  #     results[file_id]['comment'] = f"Error: {e}"
  # results = pd.DataFrame(results).T
  # return {
  #   'value': results['value'].mean(),
  #   'comment': f'based on status_code reports via HEAD',
  #   'supplement': results.to_dict() if full else pd.concat([
  #     results.head(5),
  #     results.tail(5),
  #   ]).to_dict(),
  # }

#%%
@rubric.metric({
  '@id': 136,
  'name': 'Program name',
  'description': 'Program name is available for querying',
  'detail': ''' Checks the dcc table for the dcc_name ''',
  'principle': 'Findable',
  'extended': True,
})
def _(CFDE, **kwargs):
  try:
    if 'dcc' in CFDE.tables:
      dcc = CFDE.tables['dcc']
    elif 'primary_dcc_contact' in CFDE.tables:
      logger.warning('Detected legacy table primary_dcc_contact, please move to dcc')
      dcc = CFDE.tables['primary_dcc_contact']
    else:
      raise Exception('dcc table not found')
    primary_dcc_contact = one(dcc.entities())
    return {
      'value': 1.0,
      'comment': f"Program name identified: {primary_dcc_contact['dcc_name']}"
    }
  except Exception as e:
    return {
      'value': 0.0,
      'comment': f"Program name could not be identified, error: {e}"
    }

@rubric.metric({
  '@id': 137,
  'name': 'Project name',
  'description': 'Project name is available for querying',
  'detail': ''' Checks the dcc table for the project, and then the project table for its name ''',
  'principle': 'Findable',
  'extended': True,
})
def _(CFDE, **kwargs):
  try:
    if 'dcc' in CFDE.tables:
      dcc = CFDE.tables['dcc']
    elif 'primary_dcc_contact' in CFDE.tables:
      logger.warning('Detected legacy table primary_dcc_contact, please move to dcc')
      dcc = CFDE.tables['primary_dcc_contact']
    else:
      raise Exception('dcc table not found')
    primary_dcc_contact = one(dcc.entities())
    return {
      'value': 1.0,
      'comment': f"Project name identified: {primary_dcc_contact['dcc_name']}"
    }
  except Exception as e:
    return {
      'value': 0.0,
      'comment': f"Project name could not be identified, error: {e}"
    }

#%%
@rubric.metric({
  '@id': 27,
  'name': 'PI Contact',
  'description': 'PI Contact is available for dataset',
  'detail': ''' Checks the primary_dcc_contact table for the contact_name and contact_email entries ''',
  'principle': 'Reusable',
  'extended': True,
})
def _(CFDE, **kwargs):
  try:
    if 'dcc' in CFDE.tables:
      dcc = CFDE.tables['dcc']
    elif 'primary_dcc_contact' in CFDE.tables:
      logger.warning('Detected legacy table primary_dcc_contact, please move to dcc')
      dcc = CFDE.tables['primary_dcc_contact']
    else:
      raise Exception('dcc table not found')
    primary_dcc_contact = one(dcc.entities())
    if not primary_dcc_contact.get('contact_email'):
      raise Exception('Contact email is not present')
    return {
      'value': 1.0,
      'comment': f"PI Contact identified: {primary_dcc_contact.get('contact_name', '')} <{primary_dcc_contact['contact_email']}>"
    }
  except Exception as e:
    return {
      'value': 0.0,
      'comment': f"PI Contact could not be identified, error: {e}"
    }

#%%
@rubric.metric({
  '@id': 138,
  'name': 'Responsible institution',
  'description': 'The institution that created this dataset is available',
  'detail': ''' No information about the contributing institution is currently available in the C2M2 ''',
  'principle': 'Findable',
  'extended': True,
})
def _(CFDE, **kwargs):
  return {
    'value': 0,
    'comment': 'No information about the contributing institution is currently available in the C2M2'
  }

#%%
@rubric.metric({
  '@id': 110,
  'name': 'Access protocol',
  'description': 'The protocol for accessing the data is available and described with a URI',
  'detail': ''' The C2M2 does not provide a means of capturing information about file access ''',
  'principle': 'Accessible',
  'extended': True,
})
def _(CFDE, **kwargs):
  return {
    'value': 0,
    'comment': 'The C2M2 does not provide a means of capturing information about file access'
  }


#%%
from c2m2_assessment.ontology.parser.obo import OBOOntology
OBI = memo(lambda: OBOOntology(fetch_cache('https://raw.githubusercontent.com/obi-ontology/obi/master/views/obi.obo', 'OBI.obo')))

@rubric.metric({
  '@id': 139,
  'name': 'Assay',
  'description': 'Assay is present and a proper CFDE-specified ontological term is found in the CFDE-specified ontologies.',
  'detail': ''' Identifies the proportion of files with OBI-verifiable identifiers ''',
  'principle': 'Interoperable',
  'extended': True,
})
def _(CFDE, full=False, **kwargs):
  n_good = 0
  issues = {}
  if 'file' in CFDE.tables:
    for file in CFDE.tables['file'].entities():
      file_id = (file['id_namespace'], file['local_id'])
      assay_type = file.get('assay_type')
      if not assay_type:
        issues[file_id] = f'Missing assay_type'
      elif OBI().get(assay_type) is None:
        n_good += 0.5
        issues[file_id] = f'Not found in OBI: {assay_type}'
      else:
        n_good += 1
  n_issues = len(issues)
  issues = pd.Series(issues)
  value = n_good / (n_good + n_issues) if n_good + n_issues else float('nan')
  return {
    'value': value,
    'comment': f"{n_good} / {n_good + n_issues}",
    'supplement': issues.to_dict() if full else issues.value_counts().to_dict(),
  }

#%%
from c2m2_assessment.ontology.parser.obo import OBOOntology
UBERON = memo(lambda: OBOOntology(fetch_cache('http://purl.obolibrary.org/obo/uberon.obo', 'uberon.obo')))

@rubric.metric({
  '@id': 140,
  'name': 'Anatomical Part',
  'description': 'An anatomical part is present and the CFDE-specified ontological term is found in the CFDE-specified ontologies',
  'detail': ''' Identifies the proportion of biosamples with UBERON-verifiable identifiers ''',
  'principle': 'Interoperable',
  'extended': True,
})
def _(CFDE, full=False, **kwargs):
  n_good = 0
  issues = {}
  if 'biosample' in CFDE.tables:
    for biosample in CFDE.tables['biosample'].entities():
      biosample_id = (biosample['id_namespace'], biosample['local_id'])
      anatomy = biosample.get('anatomy')
      if not anatomy:
        issues[biosample_id] = f'Missing anatomy'
      elif UBERON().get(anatomy) is None:
        n_good += 0.5
        issues[biosample_id] = f'Not found in OBI: {anatomy}'
      else:
        n_good += 1
  n_issues = len(issues)
  issues = pd.Series(issues)
  value = n_good / (n_good + n_issues) if n_good + n_issues else float('nan')
  return {
    'value': value,
    'comment': f"{n_good} / {n_good + n_issues}",
    'supplement': issues.to_dict() if full else issues.value_counts().to_dict(),
  }

#%%
from c2m2_assessment.ontology.parser.obo import OBOOntology
DOID = memo(lambda: OBOOntology(fetch_cache('https://github.com/DiseaseOntology/HumanDiseaseOntology/raw/main/src/ontology/releases/doid.obo', 'doid.obo')))

@rubric.metric({
  '@id': 141,
  'name': 'Disease',
  'description': 'A disease is present and the CFDE-specified ontological term is found in the CFDE-specified ontologies',
  'detail': ''' Identifies the proportion of subject_disease/biosample_diseases with DOID-verifiable identifiers ''',
  'principle': 'Interoperable',
  'extended': True,
})
def _(CFDE, full=False, **kwargs):
  n_good = 0
  issues = {}
  if 'subject_disease' in CFDE.tables:
    for subject_disease in CFDE.tables['subject_disease'].entities():
      subject_id = ('subject', subject_disease['subject_id_namespace'], subject_disease['subject_local_id'])
      disease = subject_disease.get('disease')
      if not disease:
        issues[subject_id] = f'Missing disease'
      elif DOID().get(disease) is None:
        n_good += 0.5
        issues[subject_id] = f'Not found in OBI: {disease}'
      else:
        n_good += 1
  if 'biosample_disease' in CFDE.tables:
    for biosample_disease in CFDE.tables['biosample_disease'].entities():
      biosample_id = ('biosample', biosample_disease['biosample_id_namespace'], biosample_disease['biosample_local_id'])
      disease = biosample_disease.get('disease')
      if not disease:
        issues[biosample_id] = f'Missing disease'
      elif DOID().get(disease) is None:
        n_good += 0.5
        issues[biosample_id] = f'Not found in OBI: {disease}'
      else:
        n_good += 1
  n_issues = len(issues)
  issues = pd.Series(issues)
  value = n_good / (n_good + n_issues) if n_good + n_issues else float('nan')
  return {
    'value': value,
    'comment': f"{n_good} / {n_good + n_issues}",
    'supplement': issues.to_dict() if full else issues.value_counts().to_dict(),
  }

#%%
from c2m2_assessment.ontology.parser.obo import OBOOntology
EDAM = memo(lambda: OBOOntology(fetch_cache('http://edamontology.org/EDAM.obo', 'EDAM.obo')))

@rubric.metric({
  '@id': 142,
  'name': 'File type',
  'description': 'A file type is present and the CFDE-specified ontological term is found in the CFDE-specified ontologies',
  'detail': ''' Identifies the proportion of files with EDAM-verifiable file_format and data_type term identifiers ''',
  'principle': 'Interoperable',
  'extended': True,
})
def _(CFDE, full=False, **kwargs):
  n_good = 0
  issues = {}
  if 'file' in CFDE.tables:
    for file in CFDE.tables['file'].entities():
      file_id = (file['id_namespace'], file['local_id'])
      file_format = file.get('file_format')
      data_type = file.get('data_type')
      file_issues = {}
      if not file_format:
        file_issues.update({
          'file_format': f'Missing file_format'
        })
      elif EDAM().get(f"EDAM_{file_format}") is None:
        n_good += 0.5
        file_issues.update({
          'file_format': f'Not found in EDAM: {file_format}'
        })
      if not data_type:
        file_issues.update({
          'data_type': f'Missing data_type'
        })
      elif EDAM().get(f"EDAM_{data_type}") is None:
        n_good += 0.5
        file_issues.update({
          'data_type': f'Not found in EDAM: {data_type}'
        })
      if file_issues:
        issues[file_id] = file_issues
      else:
        n_good += 1
  n_issues = len(issues)
  issues = pd.DataFrame(issues)
  value = n_good / (n_good + n_issues) if n_good + n_issues else float('nan')
  return {
    'value': value,
    'comment': f"{n_good} / {n_good + n_issues}",
    'supplement': issues.to_dict() if full else issues.value_counts().to_dict(), # "unhashable type: 'dict' i think it must be part of the to_dict method?
  }

#%%
from c2m2_assessment.ontology.client.ncbi_taxon import NCBITaxonClient
NCBITaxon = memo(lambda: NCBITaxonClient())

@rubric.metric({
  '@id': 143,
  'name': 'Taxonomy',
  'description': 'A taxonomy is present and the CFDE-specified ontological term is found in the CFDE-specified ontologies',
  'detail': ''' Identifies the proportion of subjects with NCBITaxon-verifiable Taxonomies ''',
  'principle': 'Interoperable',
  'extended': True,
})
def _(CFDE, full=False, **kwargs):
  n_good = 0
  issues = {}
  if 'subject_role_taxonomy' in CFDE.tables:
    for subject_role_taxonomy in CFDE.tables['subject_role_taxonomy'].entities():
      subject_id = (subject_role_taxonomy['subject_id_namespace'], subject_role_taxonomy['subject_local_id'])
      taxonomy_id = subject_role_taxonomy.get('taxonomy_id')
      if not taxonomy_id:
        issues[subject_id] = f'Missing taxonomy'
      elif NCBITaxon().get(taxonomy_id) is None:
        n_good += 0.5
        issues[subject_id] = f'Not found in ncbitaxon: {taxonomy_id}'
      else:
        n_good += 1
  issues = pd.Series(issues)
  n_subjects = CFDE.tables['subject'].count()
  value = n_good / n_subjects if n_subjects else float('nan')
  return {
    'value': value,
    'comment': f"{n_good} / {n_subjects}",
    'supplement': issues.to_dict() if full else issues.value_counts().to_dict(),
  }

#%%
from c2m2_assessment.ontology.parser.cellosaurus import CellosaurusOntology
SUBJECT_GRANULARITY_CELL_LINE = 'cfde_subject_granularity:4'
Cellosaurus = memo(lambda: CellosaurusOntology(fetch_cache('ftp://ftp.expasy.org/databases/cellosaurus/cellosaurus.xml', 'cellosaurus.xml')))

@rubric.metric({
  '@id': 144,
  'name': 'Cell Line',
  'description': 'A cell line is present and the CFDE-specified ontological term is found in the CFDE-specified ontologies',
  'detail': ''' Identifies the proportion of subjects of granularity: cell line with Cellosaurus-verifiable cell-lines ''',
  'principle': 'Interoperable',
  'extended': True,
})
def _(CFDE, full=False, **kwargs):
  n_good = 0
  issues = {}
  if 'subject' in CFDE.tables:
    for subject in CFDE.tables['subject'].filter(CFDE.tables['subject'].granularity == SUBJECT_GRANULARITY_CELL_LINE).entities():
      subject_id = (subject['id_namespace'], subject['local_id'])
      persistent_id = subject.get('persistent_id')
      if not persistent_id:
        issues[subject_id] = f'Missing persistent_id for cell line'
      elif Cellosaurus().get(persistent_id) is None:
        n_good += 0.5
        issues[subject_id] = f'Not found in Cellosaurus: {persistent_id}'
      else:
        n_good += 1
  n_issues = len(issues)
  issues = pd.Series(issues)
  value = n_good / (n_good + n_issues) if n_good + n_issues else float('nan')
  return {
    'value': value,
    'comment': f"{n_good} / {n_good + n_issues}",
    'supplement': issues.to_dict() if full else issues.value_counts().to_dict(),
  }

#%%
@rubric.metric({
  '@id': 116,
  'name': 'Data Usage License',
  'description': 'A Data usage license is described',
  'detail': ''' No information about data usage licenses are described in the C2M2 ''',
  'principle': 'Reusable',
  'extended': True,
})
def _(CFDE, **kwargs):
  return {
    'value': 0,
    'comment': 'No information about data usage licenses are described in the C2M2'
  }

#%%
@rubric.metric({
  '@id': 108,
  'name': 'Resource identifier',
  'description': 'An identifier for the resource is present',
  'detail': ''' C2M2 requires files to declare a unique resource identifier ''',
  'principle': 'Findable',
  'extended': True,
})
def _(CFDE, **kwargs):
  return {
    'value': 1.0,
    'comment': 'C2M2 requires files to declare a unique resource identifier'
  }

#%%
from c2m2_assessment.ontology.client.pubchem import PubChemSubstanceSIDClient
PubChemSubstances = memo(lambda: PubChemSubstanceSIDClient())

@rubric.metric({
  '@id': -30,
  'name': 'Substance',
  'description': 'A substance is associated and the CFDE-specified ontological term is found in the CFDE-specified ontologies',
  'detail': ''' Identifies the proportion of substances with PubChem-verifiable substance identifiers ''',
  'principle': 'Interoperable',
  'extended': True,
})
def _(CFDE, full=False, **kwargs):
  n_good = 0
  issues = {}
  if 'biosample_substance' in CFDE.tables:
    for biosample_substance in CFDE.tables['biosample_substance'].entities():
      biosample_substance_id = (biosample_substance['biosample_id_namespace'], biosample_substance['biosample_local_id'], biosample_substance['substance'])
      substance = biosample_substance.get('substance')
      if not substance:
        issues[biosample_substance_id] = f'Missing substance for biosample_substance'
      elif PubChemSubstances().get(substance) is None:
        n_good += 0.5
        issues[biosample_substance_id] = f'Not found in PubChem Substances: {substance}'
      else:
        n_good += 1
  if 'subject_substance' in CFDE.tables:
    for subject_substance in CFDE.tables['subject_substance'].entities():
      subject_substance_id = (subject_substance['subject_id_namespace'], subject_substance['subject_local_id'], subject_substance['substance'])
      substance = subject_substance.get('substance')
      if not substance:
        issues[subject_substance_id] = f'Missing substance for subject_substance'
      elif PubChemSubstances().get(substance) is None:
        n_good += 0.5
        issues[subject_substance_id] = f'Not found in PubChem Substances: {substance}'
      else:
        n_good += 1
  n_issues = len(issues)
  issues = pd.Series(issues)
  value = n_good / (n_good + n_issues) if n_good + n_issues else float('nan')
  return {
    'value': value,
    'comment': f"{n_good} / {n_good + n_issues}",
    'supplement': issues.to_dict() if full else issues.value_counts().to_dict(),
  }

#%%
from c2m2_assessment.ontology.client.pubchem import PubChemCompoundCIDClient
PubChemCompounds = memo(lambda: PubChemCompoundCIDClient())

@rubric.metric({
  '@id': -31,
  'name': 'Compound',
  'description': 'A compound is associated and the CFDE-specified ontological term is found in the CFDE-specified ontologies',
  'detail': ''' Identifies the proportion of substances with PubChem-verifiable compound identifiers ''',
  'principle': 'Interoperable',
  'extended': True,
})
def _(CFDE, full=False, **kwargs):
  n_good = 0
  issues = {}
  if 'substance' in CFDE.tables:
    for substance in CFDE.tables['substance'].entities():
      substance_id = substance['id']
      compound = substance.get('compound')
      if not compound:
        issues[substance_id] = f'Missing compound for substance'
      elif PubChemCompounds().get(compound) is None:
        n_good += 0.5
        issues[substance_id] = f'Not found in PubChem Compounds: {compound}'
      else:
        n_good += 1
  n_issues = len(issues)
  issues = pd.Series(issues)
  value = n_good / (n_good + n_issues) if n_good + n_issues else float('nan')
  return {
    'value': value,
    'comment': f"{n_good} / {n_good + n_issues}",
    'supplement': issues.to_dict() if full else issues.value_counts().to_dict(),
  }

#%%
from c2m2_assessment.ontology.client.ensembl import EnsemblClient
Ensembl = memo(lambda: EnsemblClient())

@rubric.metric({
  '@id': -32,
  'name': 'Gene',
  'description': 'A gene is associated and the CFDE-specified ontological term is found in the CFDE-specified ontologies',
  'detail': ''' Identifies the proportion of genes with Ensembl-verifiable gene identifiers ''',
  'principle': 'Interoperable',
  'extended': True,
})
def _(CFDE, full=False, **kwargs):
  n_good = 0
  issues = {}
  if 'biosample_gene' in CFDE.tables:
    for biosample_gene in CFDE.tables['biosample_gene'].entities():
      biosample_gene_id = (biosample_gene['biosample_id_namespace'], biosample_gene['biosample_local_id'], biosample_gene['gene'])
      gene = biosample_gene.get('gene')
      if not gene:
        issues[biosample_gene_id] = f'Missing gene for biosample_gene'
      elif Ensembl().get(gene) is None:
        n_good += 0.5
        issues[biosample_gene_id] = f'Not found in Ensembl: {gene}'
      else:
        n_good += 1
  n_issues = len(issues)
  issues = pd.Series(issues)
  value = n_good / (n_good + n_issues) if n_good + n_issues else float('nan')
  return {
    'value': value,
    'comment': f"{n_good} / {n_good + n_issues}",
    'supplement': issues.to_dict() if full else issues.value_counts().to_dict(),
  }
