from c2m2_assessment.fairshake.rubric import Rubric

rubric = Rubric()

from c2m2_assessment.rubrics.NCE import rubric as NCERubric
rubric.metrics.update(NCERubric.metrics)

from c2m2_assessment.rubrics.FAIR import rubric as FAIRRubric
rubric.metrics.update(FAIRRubric.metrics)

from c2m2_assessment.rubrics.FAIR_2022_q4 import rubric as FAIRRubric_q4_2022
rubric.metrics.update(FAIRRubric_q4_2022.metrics)