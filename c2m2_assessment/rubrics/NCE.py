import pandas as pd
from c2m2_assessment.fairshake.rubric import Rubric
from c2m2_assessment.resolvers.CFDE_totals import (
  total_files,
  total_collections,
  total_biosamples,
  total_subjects,
  total_projects,
)

rubric = Rubric()

rubric.metric('c2m2_assessment.metrics.m_106_metadata_conformance.metric')
rubric.metric('c2m2_assessment.metrics.m_104_persistent_identifier.metric')
rubric.metric('c2m2_assessment.metrics.m_145_landing_page.metric')

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
    'numerator': total_files_associated_with_data_type,
    'denominator': total_files(CFDE),
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
    'numerator': total_files_associated_with_file_format,
    'denominator': total_files(CFDE),
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
    'numerator': total_files_associated_with_assay_type,
    'denominator': total_files(CFDE),
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
    'numerator': total_files_associated_with_anatomy,
    'denominator': total_files(CFDE),
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
    'numerator': total_files_associated_with_biosample,
    'denominator': total_files(CFDE),
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
    'numerator': total_files_associated_with_subject,
    'denominator': total_files(CFDE),
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
    'numerator': total_files_associated_with_subject_role,
    'denominator': total_files(CFDE),
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
    'numerator': total_biosamples_associated_with_ncbi_taxon,
    'denominator': total_biosamples(CFDE),
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
    'numerator': total_biosamples_associated_with_subject,
    'denominator': total_biosamples(CFDE),
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
    'numerator': total_biosamples_associated_with_file,
    'denominator': total_biosamples(CFDE),
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
    'numerator': total_biosamples_associated_with_anatomy,
    'denominator': total_biosamples(CFDE),
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
    'numerator': total_biosamples_associated_with_assay,
    'denominator': total_biosamples(CFDE),
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
    'numerator': total_subjects_associated_with_taxonomy,
    'denominator': total_subjects(CFDE),
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
    'numerator': total_subjects_associated_with_granularity,
    'denominator': total_subjects(CFDE),
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
    'numerator': total_subjects_associated_with_role_taxonomy,
    'denominator': total_subjects(CFDE),
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
    'numerator': total_subjects_associated_with_biosample,
    'denominator': total_subjects(CFDE),
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
    'numerator': total_subjects_associated_with_file,
    'denominator': total_subjects(CFDE),
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
    'numerator': total_files_not_in_collection,
    'denominator': total_files(CFDE),
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
    'numerator': total_subjects_not_in_collection,
    'denominator': total_subjects(CFDE),
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
    'numerator': total_biosamples_not_in_collection,
    'denominator': total_biosamples(CFDE),
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
    'numerator': total_projects_associated_with_anatomy,
    'denominator': total_projects(CFDE),
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
    'numerator': total_projects_associated_with_file,
    'denominator': total_projects(CFDE),
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
    'numerator': total_projects_associated_with_data_type,
    'denominator': total_projects(CFDE),
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
    'numerator': total_projects_associated_with_subject,
    'denominator': total_projects(CFDE),
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
    'numerator': len(used_anatomy_ids),
    'denominator': total,
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
    'numerator': len(used_taxonomy_ids),
    'denominator': total,
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
    'numerator': len(used_assay_type_ids),
    'denominator': total,
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
    'numerator': len(used_file_format_ids),
    'denominator': total,
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
    'numerator': len(used_data_type_ids),
    'denominator': total,
    'supplement': unused_data_type_terms.to_dict(),
  }