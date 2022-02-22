import logging
import pandas as pd
from c2m2_assessment.fairshake.rubric import Rubric
from c2m2_assessment.util.one import one
from c2m2_assessment.util.memo import memo
from c2m2_assessment.util.fetch_cache import fetch_cache
from c2m2_assessment.resolvers.CFDE_totals import total_subjects

logger = logging.getLogger(__name__)

rubric = Rubric()

rubric.metric('c2m2_assessment.metrics.m_106_metadata_conformance.metric')
rubric.metric('c2m2_assessment.metrics.m_104_persistent_identifier.metric')
rubric.metric('c2m2_assessment.metrics.m_145_landing_page.metric')

#%%
@rubric.metric({
  '@id': 136,
  'name': 'Program name',
  'description': 'Program name is available for querying',
  'detail': ''' Checks the dcc table for the dcc_name ''',
  'principle': 'Findable',
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
    'numerator': n_good,
    'denominator': n_good + n_issues,
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
    'numerator': n_good,
    'denominator': n_good + n_issues,
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
    'numerator': n_good,
    'denominator': n_good + n_issues,
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
    'numerator': n_good,
    'denominator': n_good + n_issues,
    'supplement': issues.to_dict() if full else issues.value_counts().to_dict(),
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
  n_subjects = total_subjects(CFDE)
  value = n_good / n_subjects if n_subjects else float('nan')
  return {
    'value': value,
    'numerator': n_good,
    'denominator': n_subjects,
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
    'numerator': n_good,
    'denominator': n_good + n_issues,
    'supplement': issues.to_dict() if full else issues.value_counts().to_dict(),
  }

#%%
@rubric.metric({
  '@id': 116,
  'name': 'Data Usage License',
  'description': 'A Data usage license is described',
  'detail': ''' No information about data usage licenses are described in the C2M2 ''',
  'principle': 'Reusable',
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
    'numerator': n_good,
    'denominator': n_good + n_issues,
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
    'numerator': n_good,
    'denominator': n_good + n_issues,
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
    'numerator': n_good,
    'denominator': n_good + n_issues,
    'supplement': issues.to_dict() if full else issues.value_counts().to_dict(),
  }
