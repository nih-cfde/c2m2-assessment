# c2m2-assessment

This application may be used for performing assessments on C2M2 datapackages.

The main aspect of the assessment is in [c2m2_assessment.rubric](./c2m2_assessment/rubric.py).

## Installation
```python
pip install c2m2_assessment @ git+https://github.com/nih-cfde/c2m2-assessment
```

## Usage

### CLI
```bash
# review the options
c2m2-assessment --help
# perform a basic assessment
c2m2-assessment -v -i datapackage.zip -o results.json
```

### Python
```python
from c2m2_assessment.rubric import rubric
# FAIRshake-style Rubric object capable of performing assessment
results = list(rubric.assess([CFDE_client]))
```
