# c2m2-assessment

This application may be used for performing assessments on C2M2 datapackages.

## Installation
```python
pip install "c2m2-assessment @ git+https://github.com/nih-cfde/c2m2-assessment"
```

## Usage

A more concrete example of executing the assessment can be found [here](./example.md).

### CLI
```bash
# review the options
c2m2-assessment --help
# perform a basic assessment
c2m2-assessment -v -i datapackage.zip -o results.json
```

### Docker
```bash
# build the docker image
docker build -it c2m2-assessment .
# run the image the same way you would the python cli
docker run -w /work -v $(pwd):/work -it c2m2-assessment -i datapackage.zip -o results.json
```

### Python
```python
# or see, __main__.py
from c2m2_assessment.rubrics.NCE import rubric
# FAIRshake-style Rubric object capable of performing assessment
results = list(rubric.assess([CFDE_client]))
```
