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

rubric.metric('c2m2_assessment.metrics.m_fairshake_106_metadata_conformance.metric')
rubric.metric('c2m2_assessment.metrics.m_fairshake_104_persistent_identifier.metric')
rubric.metric('c2m2_assessment.metrics.m_fairshake_145_landing_page.metric')

@rubric.metric({
  '@id': 'cfde_fair:33',
  'name': 'biosamples with substance',
  'description': 'What ratio of biosamples are assiciated with a substance',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = None
  if 'biosample' in CFDE.tables and 'biosample_substance' in CFDE.tables:
    total_associated = CFDE.tables['biosample'] \
      .link(CFDE.tables['biosample_substance'], 
        on=(CFDE.tables['biosample_substance'].biosample_local_id == CFDE.tables['biosample'].local_id) 
          & (CFDE.tables['biosample_substance'].biosample_id_namespace == CFDE.tables['biosample'].id_namespace)
      ).groupby(CFDE.tables['biosample'].id_namespace, CFDE.tables['biosample'].local_id).count()
    total = total_biosamples(CFDE)
    value = (total_associated / total) if total else None
  return {
    'value': value,
    'numerator': total_associated,
    'denominator': total,
  }

@rubric.metric({
  '@id': 'cfde_fair:34',
  'name': 'collections with gene',
  'description': 'What ratio of collections are assigned a gene',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = None
  if 'collection' in CFDE.tables and 'collection_gene' in CFDE.tables:
    total_associated = CFDE.tables['collection'] \
      .link(CFDE.tables['collection_gene'], 
        on=(CFDE.tables['collection_gene'].collection_local_id == CFDE.tables['collection'].local_id) 
          & (CFDE.tables['collection_gene'].collection_id_namespace == CFDE.tables['collection'].id_namespace)
      ).groupby(CFDE.tables['collection'].id_namespace, CFDE.tables['collection'].local_id).count()
    total = total_collections(CFDE)
    value = (total_associated / total) if total else None
  return {
    'value': value,
    'numerator': total_associated,
    'denominator': total,
  }

@rubric.metric({
  '@id': 'cfde_fair:35',
  'name': 'collections with substance',
  'description': 'What ratio of collections are assigned a substance',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = None
  if 'collection' in CFDE.tables and 'collection_substance' in CFDE.tables:
    total_associated = CFDE.tables['collection'] \
      .link(CFDE.tables['collection_substance'], 
        on=(CFDE.tables['collection_substance'].collection_local_id == CFDE.tables['collection'].local_id) 
          & (CFDE.tables['collection_substance'].collection_id_namespace == CFDE.tables['collection'].id_namespace)
      ).groupby(CFDE.tables['collection'].id_namespace, CFDE.tables['collection'].local_id).count()
    total = total_collections(CFDE)
    value = (total_associated / total) if total else None
  return {
    'value': value,
    'numerator': total_associated,
    'denominator': total,
  }

@rubric.metric({
  '@id': 'cfde_fair:36',
  'name': 'subjects with substance',
  'description': 'What ratio of subjects are associated with a substance',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = None
  if 'subject' in CFDE.tables and 'subject_substance' in CFDE.tables:
    total_associated = CFDE.tables['subject_substance'] \
      .link(CFDE.tables['subject'], 
        on=(CFDE.tables['subject_substance'].subject_local_id == CFDE.tables['subject'].local_id) 
          & (CFDE.tables['subject_substance'].subject_id_namespace == CFDE.tables['subject'].id_namespace)
      ).groupby(CFDE.tables['subject'].id_namespace, CFDE.tables['subject'].local_id).count()
    total = total_subjects(CFDE)
    value = (total_associated / total) if total else None
  return {
    'value': value,
    'numerator': total_associated,
    'denominator': total,
  }

@rubric.metric({
  '@id': 'cfde_fair:37',
  'name': 'biosamples with gene',
  'description': 'What ratio of biosamples are associated with at least one gene',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = None
  if 'biosample' in CFDE.tables and 'biosample_gene' in CFDE.tables:
    total_associated = CFDE.tables['biosample'] \
      .link(CFDE.tables['biosample_gene'], 
        on=(CFDE.tables['biosample_gene'].biosample_local_id == CFDE.tables['biosample'].local_id) 
          & (CFDE.tables['biosample_gene'].biosample_id_namespace == CFDE.tables['biosample'].id_namespace)
      ).groupby(CFDE.tables['biosample'].id_namespace, CFDE.tables['biosample'].local_id).count()
    total = total_biosamples(CFDE)
    value = (total_associated / total) if total else None
  return {
    'value': value,
    'numerator': total_associated,
    'denominator': total,
  }

@rubric.metric({
  '@id': 'cfde_fair:38',
  'name': 'phenotypes with gene',
  'description': 'What ratio of phenotypes are associated with a gene',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = None
  if 'phenotype' in CFDE.tables and 'phenotype_gene' in CFDE.tables:
    total_associated = CFDE.tables['phenotype_gene'] \
      .link(CFDE.tables['phenotype'], on=(
        CFDE.tables['phenotype'].id == CFDE.tables['phenotype_gene'].phenotype
      )).groupby(CFDE.tables['phenotype'].id).count()
    total = total_phenotypes(CFDE)
    value = (total_associated / total) if total else None
  return {
    'value': value,
    'numerator': total_associated,
    'denominator': total,
  }

@rubric.metric({
  '@id': 'cfde_fair:39',
  'name': 'proteins with gene',
  'description': 'What ratio of proteins are associated with a gene',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = None
  if 'protein' in CFDE.tables and 'protein_gene' in CFDE.tables:
    total_associated = CFDE.tables['protein_gene'] \
      .link(CFDE.tables['protein'], on=(
        CFDE.tables['protein'].id == CFDE.tables['protein_gene'].protein
      )).groupby(CFDE.tables['protein'].id).count()
    total = total_proteins(CFDE)
    value = (total_associated / total) if total else None
  return {
    'value': value,
    'numerator': total_associated,
    'denominator': total,
  }


@rubric.metric({
  '@id': 'cfde_fair:40',
  'name': 'collections with protein',
  'description': 'What ratio of collections are associated with at least one gene',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = None
  if 'collection' in CFDE.tables and 'collection_protein' in CFDE.tables:
    total_associated = CFDE.tables['collection'] \
      .link(CFDE.tables['collection_protein'], 
        on=(CFDE.tables['collection_protein'].collection_local_id == CFDE.tables['collection'].local_id) 
          & (CFDE.tables['collection_protein'].collection_id_namespace == CFDE.tables['collection'].id_namespace)
      ).groupby(CFDE.tables['collection'].id_namespace, CFDE.tables['collection'].local_id).count()
    total = total_collections(CFDE)
    value = (total_associated / total) if total else None
  return {
    'value': value,
    'numerator': total_associated,
    'denominator': total,
  }

@rubric.metric({
  '@id': 'cfde_fair:41',
  'name': 'subjects with phenotype',
  'description': 'What ratio of subjects are associated with a phenotype',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = None
  if 'subject' in CFDE.tables and 'subject_phenotype' in CFDE.tables:
    total_associated = CFDE.tables['subject_phenotype'] \
      .link(CFDE.tables['subject'], on=((
        CFDE.tables['subject'].local_id == CFDE.tables['subject_phenotype'].subject_local_id
      ) & (
        CFDE.tables['subject'].id_namespace == CFDE.tables['subject_phenotype'].subject_id_namespace
      ))).groupby(CFDE.tables['subject'].id_namespace, CFDE.tables['subject'].local_id).count()
    total = total_subjects(CFDE)
    value = (total_associated / total) if total else None
  return {
    'value': value,
    'numerator': total_associated,
    'denominator': total,
  }

@rubric.metric({
  '@id': 'cfde_fair:42',
  'name': 'genes with phenotype',
  'description': 'What ratio of genes are associated with a phenotype',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = None
  if 'gene' in CFDE.tables and 'phenotype_gene' in CFDE.tables:
    total_associated = CFDE.tables['phenotype_gene'] \
      .link(CFDE.tables['gene'], on=(
        CFDE.tables['gene'].id == CFDE.tables['phenotype_gene'].gene
      )).groupby(CFDE.tables['gene'].id).count()
    total = total_genes(CFDE)
    value = (total_associated / total) if total else None
  return {
    'value': value,
    'numerator': total_associated,
    'denominator': total,
  }

@rubric.metric({
  '@id': 'cfde_fair:43',
  'name': 'diseases with phenotype',
  'description': 'What ratio of diseases are associated with a phenotype',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = None
  if 'disease' in CFDE.tables and 'phenotype_disease' in CFDE.tables:
    total_associated = CFDE.tables['phenotype_disease'] \
      .link(CFDE.tables['disease'], on=(
        CFDE.tables['disease'].id == CFDE.tables['phenotype_disease'].disease
      )).groupby(CFDE.tables['disease'].id).count()
    total = total_diseases(CFDE)
    value = (total_associated / total) if total else None
  return {
    'value': value,
    'numerator': total_associated,
    'denominator': total,
  }
  
@rubric.metric({
  '@id': 'cfde_fair:44',
  'name': 'collections with phenotype',
  'description': 'What ratio of collections are associated with a phenotype',
})
def _(CFDE, full=False, **kwargs):
  total_associated = total = 0
  value = None
  if 'collection' in CFDE.tables and 'collection_phenotype' in CFDE.tables:
    total_associated = CFDE.tables['collection'] \
      .link(CFDE.tables['collection_phenotype'], 
        on=(CFDE.tables['collection_phenotype'].collection_local_id == CFDE.tables['collection'].local_id) 
          & (CFDE.tables['collection_phenotype'].collection_id_namespace == CFDE.tables['collection'].id_namespace)
      ).groupby(CFDE.tables['collection'].id_namespace, CFDE.tables['collection'].local_id).count()
    total = total_collections(CFDE)
    value = (total_associated / total) if total else None
  return {
    'value': value,
    'numerator': total_associated,
    'denominator': total,
  }
