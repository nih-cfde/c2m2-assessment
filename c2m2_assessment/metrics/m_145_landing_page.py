from c2m2_assessment.fairshake.metric import Metric

@Metric.create({
  '@id': 'fairshake:145',
  'name': 'Landing Page',
  'description': 'A landing page exists and is accessible for the identifiers',
  'detail': '''Checks to make sure the persistent_id is resolvable with a HEAD request. if it is not http/https it is assumed to be an identifiers.org-resolvable CURIE. note that this is still error prone, some identifier websites do not follow HTTP standards and may not report 404s with ids that aren't found.''',
  'principle': 'Findable',
  'extended': True,
})
def metric(CFDE, full=False, **kwargs):
  return {
    'value': None,
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
