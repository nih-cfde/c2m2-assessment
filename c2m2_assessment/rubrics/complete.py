from c2m2_assessment.fairshake.rubric import Rubric

rubric = Rubric()

from c2m2_assessment.rubrics.NCE import rubric as NCERubric
rubric.metrics.update(NCERubric.metrics)

from c2m2_assessment.rubrics.FAIR import rubric as FAIRRubric
rubric.metrics.update(FAIRRubric.metrics)
