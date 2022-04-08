import pandas as pd
from c2m2_assessment.fairshake.rubric import Rubric
from c2m2_assessment.resolvers.CFDE_totals import (
  total_files,
  total_collections,
  total_biosamples,
  total_subjects,
  total_projects,
  total_genes,
  total_phenotypes,
  total_proteins,
  total_diseases
)

rubric = Rubric()

rubric.metric('c2m2_assessment.metrics.m_106_metadata_conformance.metric')
rubric.metric('c2m2_assessment.metrics.m_104_persistent_identifier.metric')
rubric.metric('c2m2_assessment.metrics.m_145_landing_page.metric')

@rubric.metric({
  '@id': -33,
  'name': 'Ratio of biosamples associated with a substance',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = float('nan')
  if 'biosample' in CFDE.tables and 'biosample_substance' in CFDE.tables:
    total_associated = CFDE.tables['biosample'] \
      .link(CFDE.tables['biosample_substance'], 
        on=(CFDE.tables['biosample_substance'].biosample_local_id == CFDE.tables['biosample'].local_id) 
          & (CFDE.tables['biosample_substance'].biosample_id_namespace == CFDE.tables['biosample'].id_namespace)
      ).groupby(CFDE.tables['biosample'].id_namespace, CFDE.tables['biosample'].local_id).count()
    total = total_biosamples(CFDE)
    value = (total_associated / total) if total else float('nan')
  return {
    'value': value,
    'comment': f"{total_associated} / {total}",
  }

@rubric.metric({
  '@id': -34,
  'name': 'Ratio of collections that are assigned a gene',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = float('nan')
  if 'collection' in CFDE.tables and 'collection_gene' in CFDE.tables:
    total_associated = CFDE.tables['collection'] \
      .link(CFDE.tables['collection_gene'], 
        on=(CFDE.tables['collection_gene'].collection_local_id == CFDE.tables['collection'].local_id) 
          & (CFDE.tables['collection_gene'].collection_id_namespace == CFDE.tables['collection'].id_namespace)
      ).groupby(CFDE.tables['collection'].id_namespace, CFDE.tables['collection'].local_id).count()
    total = total_collections(CFDE)
    value = (total_associated / total) if total else float('nan')
  return {
    'value': value,
    'comment': f"{total_associated} / {total}",
  }

@rubric.metric({
  '@id': -35,
  'name': 'Ratio of collections that are assigned a substance',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = float('nan')
  if 'collection' in CFDE.tables and 'collection_substance' in CFDE.tables:
    total_associated = CFDE.tables['collection'] \
      .link(CFDE.tables['collection_substance'], 
        on=(CFDE.tables['collection_substance'].collection_local_id == CFDE.tables['collection'].local_id) 
          & (CFDE.tables['collection_substance'].collection_id_namespace == CFDE.tables['collection'].id_namespace)
      ).groupby(CFDE.tables['collection'].id_namespace, CFDE.tables['collection'].local_id).count()
    total = total_collections(CFDE)
    value = (total_associated / total) if total else float('nan')
  return {
    'value': value,
    'comment': f"{total_associated} / {total}",
  }

@rubric.metric({
  '@id': -36,
  'name': 'Ratio of subjects associated with a substance',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = float('nan')
  if 'subject' in CFDE.tables and 'subject_substance' in CFDE.tables:
    total_associated = CFDE.tables['subject_substance'] \
      .link(CFDE.tables['subject'], 
        on=(CFDE.tables['subject_substance'].subject_local_id == CFDE.tables['subject'].local_id) 
          & (CFDE.tables['subject_substance'].subject_id_namespace == CFDE.tables['subject'].id_namespace)
      ).groupby(CFDE.tables['subject'].id_namespace, CFDE.tables['subject'].local_id).count()
    total = total_subjects(CFDE)
    value = (total_associated / total) if total else float('nan')
  return {
    'value': value,
    'comment': f"{total_associated} / {total}",
  }

@rubric.metric({
  '@id': -37,
  'name': 'Ratio of biosamples assigned to a gene',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = float('nan')
  if 'biosample' in CFDE.tables and 'biosample_gene' in CFDE.tables:
    total_associated = CFDE.tables['biosample'] \
      .link(CFDE.tables['biosample_gene'], 
        on=(CFDE.tables['biosample_gene'].biosample_local_id == CFDE.tables['biosample'].local_id) 
          & (CFDE.tables['biosample_gene'].biosample_id_namespace == CFDE.tables['biosample'].id_namespace)
      ).groupby(CFDE.tables['biosample'].id_namespace, CFDE.tables['biosample'].local_id).count()
    total = total_biosamples(CFDE)
    value = (total_associated / total) if total else float('nan')
  return {
    'value': value,
    'comment': f"{total_associated} / {total}",
  }

@rubric.metric({
  '@id': -38,
  'name': 'Ratio of phenotypes associated with a gene',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = float('nan')
  if 'phenotype' in CFDE.tables and 'phenotype_gene' in CFDE.tables:
    total_associated = CFDE.tables['phenotype_gene'] \
      .link(CFDE.tables['phenotype'], on=(
        CFDE.tables['phenotype'].id == CFDE.tables['phenotype_gene'].phenotype
      )).groupby(CFDE.tables['phenotype'].id).count()
    total = total_phenotypes(CFDE)
    value = (total_associated / total) if total else float('nan')
  return {
    'value': value,
    'comment': f"{total_associated} / {total}",
  }

@rubric.metric({
  '@id': -39,
  'name': 'Ratio of proteins associated with a gene',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = float('nan')
  if 'protein' in CFDE.tables and 'protein_gene' in CFDE.tables:
    total_associated = CFDE.tables['protein_gene'] \
      .link(CFDE.tables['protein'], on=(
        CFDE.tables['protein'].id == CFDE.tables['protein_gene'].protein
      )).groupby(CFDE.tables['protein'].id).count()
    total = total_proteins(CFDE)
    value = (total_associated / total) if total else float('nan')
  return {
    'value': value,
    'comment': f"{total_associated} / {total}",
  }


@rubric.metric({
  '@id': -40,
  'name': 'Ratio of collections associated with a protein',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = float('nan')
  if 'collection' in CFDE.tables and 'collection_protein' in CFDE.tables:
    total_associated = CFDE.tables['collection'] \
      .link(CFDE.tables['collection_protein'], 
        on=(CFDE.tables['collection_protein'].collection_local_id == CFDE.tables['collection'].local_id) 
          & (CFDE.tables['collection_protein'].collection_id_namespace == CFDE.tables['collection'].id_namespace)
      ).groupby(CFDE.tables['collection'].id_namespace, CFDE.tables['collection'].local_id).count()
    total = total_collections(CFDE)
    value = (total_associated / total) if total else float('nan')
  return {
    'value': value,
    'comment': f"{total_associated} / {total}",
  }

@rubric.metric({
  '@id': -41,
  'name': 'Ratio of subjects associated with a phenotype',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = float('nan')
  if 'subject' in CFDE.tables and 'subject_phenotype' in CFDE.tables:
    total_associated = CFDE.tables['subject_phenotype'] \
      .link(CFDE.tables['subject'], on=((
        CFDE.tables['subject'].local_id == CFDE.tables['subject_phenotype'].subject_local_id
      ) & (
        CFDE.tables['subject'].id_namespace == CFDE.tables['subject_phenotype'].subject_id_namespace
      ))).groupby(CFDE.tables['subject'].id_namespace, CFDE.tables['subject'].local_id).count()
    total = total_subjects(CFDE)
    value = (total_associated / total) if total else float('nan')
  return {
    'value': value,
    'comment': f"{total_associated} / {total}",
  }

@rubric.metric({
  '@id': -42,
  'name': 'Ratio of genes associated with a phenotype',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = float('nan')
  if 'gene' in CFDE.tables and 'phenotype_gene' in CFDE.tables:
    total_associated = CFDE.tables['phenotype_gene'] \
      .link(CFDE.tables['gene'], on=(
        CFDE.tables['gene'].id == CFDE.tables['phenotype_gene'].gene
      )).groupby(CFDE.tables['gene'].id).count()
    total = total_genes(CFDE)
    value = (total_associated / total) if total else float('nan')
  return {
    'value': value,
    'comment': f"{total_associated} / {total}",
  }

@rubric.metric({
  '@id': -43,
  'name': 'Ratio of Diseases associated with a phenotype',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = float('nan')
  if 'disease' in CFDE.tables and 'phenotype_disease' in CFDE.tables:
    total_associated = CFDE.tables['phenotype_disease'] \
      .link(CFDE.tables['disease'], on=(
        CFDE.tables['disease'].id == CFDE.tables['phenotype_disease'].disease
      )).groupby(CFDE.tables['disease'].id).count()
    total = total_diseases(CFDE)
    value = (total_associated / total) if total else float('nan')
  return {
    'value': value,
    'comment': f"{total_associated} / {total}",
  }
  
@rubric.metric({
  '@id': -44,
  'name': 'Ratio of collections associated with a phenotype',
  'description': '',
  'detail': '',
  'principle': '',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = float('nan')
  if 'collection' in CFDE.tables and 'collection_phenotype' in CFDE.tables:
    total_associated = CFDE.tables['collection'] \
      .link(CFDE.tables['collection_phenotype'], 
        on=(CFDE.tables['collection_phenotype'].collection_local_id == CFDE.tables['collection'].local_id) 
          & (CFDE.tables['collection_phenotype'].collection_id_namespace == CFDE.tables['collection'].id_namespace)
      ).groupby(CFDE.tables['collection'].id_namespace, CFDE.tables['collection'].local_id).count()
    total = total_collections(CFDE)
    value = (total_associated / total) if total else float('nan')
  return {
    'value': value,
    'comment': f"{total_associated} / {total}",
  }
