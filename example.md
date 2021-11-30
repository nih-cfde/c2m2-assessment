# Example

## Fetch an example datapackage
```bash
curl https://appyters.maayanlab.cloud/CFDE-C2M2-FAIR-Datapackage-Assessment/static/example.zip -o example.zip
```

```raw
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 68030  100 68030    0     0   448k      0 --:--:-- --:--:-- --:--:--  448k
```

## Perform an assessment with the compressed datapackage
```bash
c2m2-assessment -v -i example.zip -o example.json
```

```raw
INFO:c2m2_assessment.util.rubric:Target: <deriva_datapackage.DerivaCompatPkg object at 0x7fc1f1eef7f0>
INFO:c2m2_assessment.util.rubric:Metric: Metadata conformance
INFO:c2m2_assessment.util.rubric:Answer: 86.80% (See metadata coverage for more info)
INFO:c2m2_assessment.util.rubric:Metric: Persistent identifier
INFO:c2m2_assessment.util.rubric:Answer: 0.00% (0 / 422)
INFO:c2m2_assessment.util.rubric:Metric: ratio files are associated with data type term
INFO:c2m2_assessment.util.rubric:Answer: 98.34% (415 / 422)
INFO:c2m2_assessment.util.rubric:Metric: ratio files are associated with file format term
INFO:c2m2_assessment.util.rubric:Answer: 98.34% (415 / 422)
INFO:c2m2_assessment.util.rubric:Metric: ratio files are associated with assaytype term
INFO:c2m2_assessment.util.rubric:Answer: 99.05% (418 / 422)
INFO:c2m2_assessment.util.rubric:Metric: ratio files are associate with anatomy term
INFO:c2m2_assessment.util.rubric:Answer: 72.27% (305 / 422)
INFO:c2m2_assessment.util.rubric:Metric: ratio files are associated with a biosample
INFO:c2m2_assessment.util.rubric:Answer: 72.27% (305 / 422)
INFO:c2m2_assessment.util.rubric:Metric: ratio files are associated with a subject
INFO:c2m2_assessment.util.rubric:Answer: 72.27% (305 / 422)
INFO:c2m2_assessment.util.rubric:Metric: ratio files are associated with a subject_role_taxonomy
INFO:c2m2_assessment.util.rubric:Answer: 25.12% (106 / 422)
INFO:c2m2_assessment.util.rubric:Metric: ratio biosamples are associated with a species term (NCBI Taxon)
INFO:c2m2_assessment.util.rubric:Answer: 18.73% (251 / 1340)
INFO:c2m2_assessment.util.rubric:Metric: ratio biosamples are associated with a subject
INFO:c2m2_assessment.util.rubric:Answer: 100.00% (1340 / 1340)
INFO:c2m2_assessment.util.rubric:Metric: ratio biosamples are associated with a file
INFO:c2m2_assessment.util.rubric:Answer: 100.00% (1340 / 1340)
INFO:c2m2_assessment.util.rubric:Metric: ratio biosamples are associated with an anatomy term
INFO:c2m2_assessment.util.rubric:Answer: 99.85% (1338 / 1340)
INFO:c2m2_assessment.util.rubric:Metric: ratio biosamples are associated with an assay term
INFO:c2m2_assessment.util.rubric:Answer: 89.40% (1198 / 1340)
INFO:c2m2_assessment.util.rubric:Metric: ratio subjects are associated with a taxonomy
INFO:c2m2_assessment.util.rubric:Answer: 6.45% (98 / 1520)
INFO:c2m2_assessment.util.rubric:Metric: ratio subjects have subject granularity
INFO:c2m2_assessment.util.rubric:Answer: 100.00% (1520 / 1520)
INFO:c2m2_assessment.util.rubric:Metric: ratio subjects have taxonomic role
INFO:c2m2_assessment.util.rubric:Answer: 6.45% (98 / 1520)
INFO:c2m2_assessment.util.rubric:Metric: ratio subjects associated with a biosample
INFO:c2m2_assessment.util.rubric:Answer: 12.50% (190 / 1520)
INFO:c2m2_assessment.util.rubric:Metric: ratio subjects associated with a file
INFO:c2m2_assessment.util.rubric:Answer: 12.50% (190 / 1520)
INFO:c2m2_assessment.util.rubric:Metric: IF there are collections: # of files that are part of a collection
INFO:c2m2_assessment.util.rubric:Answer: 74.88% (316 / 422)
INFO:c2m2_assessment.util.rubric:Metric: IF there are collections: # of subjects that are part of a collection
INFO:c2m2_assessment.util.rubric:Answer: 12.43% (189 / 1520)
INFO:c2m2_assessment.util.rubric:Metric: IF there are collections: # of biosamples that are part of a collection
INFO:c2m2_assessment.util.rubric:Answer: 81.27% (1089 / 1340)
INFO:c2m2_assessment.util.rubric:Metric: Project associated with anatomy
INFO:c2m2_assessment.util.rubric:Answer: 87.50% (7 / 8)
INFO:c2m2_assessment.util.rubric:Metric: Project associated with files
INFO:c2m2_assessment.util.rubric:Answer: 87.50% (7 / 8)
INFO:c2m2_assessment.util.rubric:Metric: Project associated with data types
INFO:c2m2_assessment.util.rubric:Answer: 87.50% (7 / 8)
INFO:c2m2_assessment.util.rubric:Metric: Project associated with subjects
INFO:c2m2_assessment.util.rubric:Answer: 25.00% (2 / 8)
INFO:c2m2_assessment.util.rubric:Metric: list of any anatomy terms in anatomy.tsv NOT associated with biosamples
INFO:c2m2_assessment.util.rubric:Answer: 100.00% (19 / 19)
INFO:c2m2_assessment.util.rubric:Metric: list of any species terms in ncbi_taxonomy.tsv NOT associated with a subject
INFO:c2m2_assessment.util.rubric:Answer: 100.00% (1 / 1)
INFO:c2m2_assessment.util.rubric:Metric: list of any assay terms in assay_type.tsv NOT associated with files
INFO:c2m2_assessment.util.rubric:Answer: 45.00% (18 / 40)
INFO:c2m2_assessment.util.rubric:Metric: list of any format terms in file_format.tsv NOT associated with files
INFO:c2m2_assessment.util.rubric:Answer: 100.00% (4 / 4)
INFO:c2m2_assessment.util.rubric:Metric: list of any data type terms in data_type.tsv NOT associated with files
INFO:c2m2_assessment.util.rubric:Answer: 100.00% (5 / 5)
```

## Inspect output file
```bash
jq '.' example.json
```

```json
[
  {
    "value": 0.8679777778,
    "comment": "See metadata coverage for more info",
    "supplement": {
      "count": {
        "project": 8,
        "assay_type": 40,
        "file": 422,
        "biosample": 1340,
        "anatomy": 19,
        "data_type": 5,
        "file_format": 4,
        "collection": 251,
        "ncbi_taxonomy": 1,
        "subject": 1520,
        "project_in_project": 7,
        "primary_dcc_contact": 1,
        "id_namespace": 1,
        "file_describes_subject": 1505,
        "subject_in_collection": 1089,
        "file_describes_biosample": 1650,
        "collection_defined_by_project": 251,
        "biosample_in_collection": 1089,
        "biosample_from_subject": 1340,
        "file_in_collection": 316,
        "subject_role_taxonomy": 98
      },
      "mean": {
        "project": 0.5357142857,
        "assay_type": 0.6125,
        "file": 0.6966824645,
        "biosample": 0.7140724947,
        "anatomy": 0.75,
        "data_type": 0.75,
        "file_format": 0.75,
        "collection": 0.7706317587,
        "ncbi_taxonomy": 0.8,
        "subject": 0.8479323308,
        "project_in_project": 1,
        "primary_dcc_contact": 1,
        "id_namespace": 1,
        "file_describes_subject": 1,
        "subject_in_collection": 1,
        "file_describes_biosample": 1,
        "collection_defined_by_project": 1,
        "biosample_in_collection": 1,
        "biosample_from_subject": 1,
        "file_in_collection": 1,
        "subject_role_taxonomy": 1
      },
      "std": {
        "project": 0.1983900214,
        "assay_type": 0.1259578684,
        "file": 0.0604771191,
        "biosample": 0.0055169917,
        "anatomy": 0,
        "data_type": 0,
        "file_format": 0,
        "collection": 0.0722536299,
        "ncbi_taxonomy": 0,
        "subject": 0.0350965248,
        "project_in_project": 0,
        "primary_dcc_contact": 0,
        "id_namespace": 0,
        "file_describes_subject": 0,
        "subject_in_collection": 0,
        "file_describes_biosample": 0,
        "collection_defined_by_project": 0,
        "biosample_in_collection": 0,
        "biosample_from_subject": 0,
        "file_in_collection": 0,
        "subject_role_taxonomy": 0
      },
      "min": {
        "project": 0.4285714286,
        "assay_type": 0.5,
        "file": 0.5333333333,
        "biosample": 0.5714285714,
        "anatomy": 0.75,
        "data_type": 0.75,
        "file_format": 0.75,
        "collection": 0.5714285714,
        "ncbi_taxonomy": 0.8,
        "subject": 0.7142857143,
        "project_in_project": 1,
        "primary_dcc_contact": 1,
        "id_namespace": 1,
        "file_describes_subject": 1,
        "subject_in_collection": 1,
        "file_describes_biosample": 1,
        "collection_defined_by_project": 1,
        "biosample_in_collection": 1,
        "biosample_from_subject": 1,
        "file_in_collection": 1,
        "subject_role_taxonomy": 1
      },
      "25%": {
        "project": 0.4285714286,
        "assay_type": 0.5,
        "file": 0.6,
        "biosample": 0.7142857143,
        "anatomy": 0.75,
        "data_type": 0.75,
        "file_format": 0.75,
        "collection": 0.7142857143,
        "ncbi_taxonomy": 0.8,
        "subject": 0.8571428571,
        "project_in_project": 1,
        "primary_dcc_contact": 1,
        "id_namespace": 1,
        "file_describes_subject": 1,
        "subject_in_collection": 1,
        "file_describes_biosample": 1,
        "collection_defined_by_project": 1,
        "biosample_in_collection": 1,
        "biosample_from_subject": 1,
        "file_in_collection": 1,
        "subject_role_taxonomy": 1
      },
      "50%": {
        "project": 0.4285714286,
        "assay_type": 0.5,
        "file": 0.7333333333,
        "biosample": 0.7142857143,
        "anatomy": 0.75,
        "data_type": 0.75,
        "file_format": 0.75,
        "collection": 0.7142857143,
        "ncbi_taxonomy": 0.8,
        "subject": 0.8571428571,
        "project_in_project": 1,
        "primary_dcc_contact": 1,
        "id_namespace": 1,
        "file_describes_subject": 1,
        "subject_in_collection": 1,
        "file_describes_biosample": 1,
        "collection_defined_by_project": 1,
        "biosample_in_collection": 1,
        "biosample_from_subject": 1,
        "file_in_collection": 1,
        "subject_role_taxonomy": 1
      },
      "75%": {
        "project": 0.5357142857,
        "assay_type": 0.75,
        "file": 0.7333333333,
        "biosample": 0.7142857143,
        "anatomy": 0.75,
        "data_type": 0.75,
        "file_format": 0.75,
        "collection": 0.8571428571,
        "ncbi_taxonomy": 0.8,
        "subject": 0.8571428571,
        "project_in_project": 1,
        "primary_dcc_contact": 1,
        "id_namespace": 1,
        "file_describes_subject": 1,
        "subject_in_collection": 1,
        "file_describes_biosample": 1,
        "collection_defined_by_project": 1,
        "biosample_in_collection": 1,
        "biosample_from_subject": 1,
        "file_in_collection": 1,
        "subject_role_taxonomy": 1
      },
      "max": {
        "project": 0.8571428571,
        "assay_type": 0.75,
        "file": 0.7333333333,
        "biosample": 0.7142857143,
        "anatomy": 0.75,
        "data_type": 0.75,
        "file_format": 0.75,
        "collection": 0.8571428571,
        "ncbi_taxonomy": 0.8,
        "subject": 0.8571428571,
        "project_in_project": 1,
        "primary_dcc_contact": 1,
        "id_namespace": 1,
        "file_describes_subject": 1,
        "subject_in_collection": 1,
        "file_describes_biosample": 1,
        "collection_defined_by_project": 1,
        "biosample_in_collection": 1,
        "biosample_from_subject": 1,
        "file_in_collection": 1,
        "subject_role_taxonomy": 1
      }
    },
    "metric": 106,
    "name": "Metadata conformance",
    "description": "The metadata properly conforms with the CFDE perscribed metadata model specification",
    "detail": "The average metadata coverage of all tables",
    "principle": "Findable"
  },
  {
    "value": 0,
    "comment": "0 / 422",
    "supplement": {},
    "metric": 104,
    "name": "Persistent identifier",
    "description": "Globally unique, persistent, and valid identifiers (preferrably DOIs) are present for the dataset",
    "detail": "We check that the persistent id that are present are DOIs.",
    "principle": "Findable"
  },
  {
    "value": 0.9834123223,
    "comment": "415 / 422",
    "supplement": null,
    "metric": -1,
    "name": "ratio files are associated with data type term",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.9834123223,
    "comment": "415 / 422",
    "supplement": null,
    "metric": -2,
    "name": "ratio files are associated with file format term",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.990521327,
    "comment": "418 / 422",
    "supplement": null,
    "metric": -3,
    "name": "ratio files are associated with assaytype term",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.7227488152,
    "comment": "305 / 422",
    "supplement": null,
    "metric": -4,
    "name": "ratio files are associate with anatomy term",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.7227488152,
    "comment": "305 / 422",
    "supplement": null,
    "metric": -5,
    "name": "ratio files are associated with a biosample",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.7227488152,
    "comment": "305 / 422",
    "supplement": null,
    "metric": -6,
    "name": "ratio files are associated with a subject",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.2511848341,
    "comment": "106 / 422",
    "supplement": null,
    "metric": -7,
    "name": "ratio files are associated with a subject_role_taxonomy",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.1873134328,
    "comment": "251 / 1340",
    "supplement": null,
    "metric": -8,
    "name": "ratio biosamples are associated with a species term (NCBI Taxon)",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 1,
    "comment": "1340 / 1340",
    "supplement": null,
    "metric": -9,
    "name": "ratio biosamples are associated with a subject",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 1,
    "comment": "1340 / 1340",
    "supplement": null,
    "metric": -10,
    "name": "ratio biosamples are associated with a file",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.9985074627,
    "comment": "1338 / 1340",
    "supplement": null,
    "metric": -11,
    "name": "ratio biosamples are associated with an anatomy term",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.8940298507,
    "comment": "1198 / 1340",
    "supplement": null,
    "metric": -12,
    "name": "ratio biosamples are associated with an assay term",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.0644736842,
    "comment": "98 / 1520",
    "supplement": null,
    "metric": -13,
    "name": "ratio subjects are associated with a taxonomy",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 1,
    "comment": "1520 / 1520",
    "supplement": null,
    "metric": -14,
    "name": "ratio subjects have subject granularity",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.0644736842,
    "comment": "98 / 1520",
    "supplement": null,
    "metric": -15,
    "name": "ratio subjects have taxonomic role",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.125,
    "comment": "190 / 1520",
    "supplement": null,
    "metric": -16,
    "name": "ratio subjects associated with a biosample",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.125,
    "comment": "190 / 1520",
    "supplement": null,
    "metric": -17,
    "name": "ratio subjects associated with a file",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.7488151659,
    "comment": "316 / 422",
    "supplement": null,
    "metric": -18,
    "name": "IF there are collections: # of files that are part of a collection",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.1243421053,
    "comment": "189 / 1520",
    "supplement": null,
    "metric": -19,
    "name": "IF there are collections: # of subjects that are part of a collection",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.8126865672,
    "comment": "1089 / 1340",
    "supplement": null,
    "metric": -20,
    "name": "IF there are collections: # of biosamples that are part of a collection",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.875,
    "comment": "7 / 8",
    "supplement": null,
    "metric": -21,
    "name": "Project associated with anatomy",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.875,
    "comment": "7 / 8",
    "supplement": null,
    "metric": -22,
    "name": "Project associated with files",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.875,
    "comment": "7 / 8",
    "supplement": null,
    "metric": -23,
    "name": "Project associated with data types",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.25,
    "comment": "2 / 8",
    "supplement": null,
    "metric": -24,
    "name": "Project associated with subjects",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 1,
    "comment": "19 / 19",
    "supplement": {},
    "metric": -25,
    "name": "list of any anatomy terms in anatomy.tsv NOT associated with biosamples",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 1,
    "comment": "1 / 1",
    "supplement": {},
    "metric": -26,
    "name": "list of any species terms in ncbi_taxonomy.tsv NOT associated with a subject",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 0.45,
    "comment": "18 / 40",
    "supplement": {
      "id": {
        "OBI:0000366": "OBI:0000366",
        "OBI:0000424": "OBI:0000424",
        "OBI:0000470": "OBI:0000470",
        "OBI:0000615": "OBI:0000615",
        "OBI:0000854": "OBI:0000854",
        "OBI:0000891": "OBI:0000891",
        "OBI:0000893": "OBI:0000893",
        "OBI:0001146": "OBI:0001146",
        "OBI:0001501": "OBI:0001501",
        "OBI:0001977": "OBI:0001977",
        "OBI:0002020": "OBI:0002020",
        "OBI:0002039": "OBI:0002039",
        "OBI:0002082": "OBI:0002082",
        "OBI:0002948": "OBI:0002948",
        "OBI:0002955": "OBI:0002955",
        "OBI:0002956": "OBI:0002956",
        "OBI:0002957": "OBI:0002957",
        "OBI:0002958": "OBI:0002958",
        "OBI:0002968": "OBI:0002968",
        "OBI:0002969": "OBI:0002969",
        "OBI:0002970": "OBI:0002970",
        "OBI:0200198": "OBI:0200198"
      },
      "name": {
        "OBI:0000366": "metabolite profiling assay",
        "OBI:0000424": "transcription profiling assay",
        "OBI:0000470": "mass spectrometry assay",
        "OBI:0000615": "protein expression profiling assay",
        "OBI:0000854": "protein expression profiling",
        "OBI:0000891": "cell proliferation assay",
        "OBI:0000893": "real time polymerase chain reaction assay",
        "OBI:0001146": "binding assay",
        "OBI:0001501": "fluorescence detection assay",
        "OBI:0001977": "cytometry assay",
        "OBI:0002020": "epigenetic modification assay",
        "OBI:0002039": "assay for transposase-accessible chromatin using sequencing",
        "OBI:0002082": "reporter gene assay",
        "OBI:0002948": "fluorescence imaging based cell cycle state assay (provisional OBI term)",
        "OBI:0002955": "mass spectrometry protein state assay (provisional OBI term)",
        "OBI:0002956": "P100 protein and phosphoprotein quantification assay (provisional OBI term)",
        "OBI:0002957": "reverse phase protein array profiling assay (provisional OBI term)",
        "OBI:0002958": "SWATH-MS protein profiling assay (provisional OBI term)",
        "OBI:0002968": "positive/negative ion switching metabolite profiling assay (provisional OBI term)",
        "OBI:0002969": "cyclic immunofluorescence (provisional OBI term)",
        "OBI:0002970": "bead-based immunoassay for protein state (provisional OBI term)",
        "OBI:0200198": "tandem mass spectrometry"
      },
      "description": {
        "OBI:0000366": "An assay that detects and identifies chemical entities resulting from biochemical and cellular metabolism",
        "OBI:0000424": "An assay that determines gene expression and transcription activity using ribonucleic acids collected from a material entity.",
        "OBI:0000470": "An assay that identifies the amount and type of material entities present in a sample by fragmenting the sample and measuring the mass-to-charge ratio of the resulting particles.",
        "OBI:0000615": "An assay that determines protein expression and translation activity using protein extracts collected from a material entity.",
        "OBI:0000854": "An analyte assay that detects specific peptides in an input material by separating it using gel electrophoresis, transfering the separated molecules to a membrane, and staining them with_ antibodies specific to the analyte molecules.",
        "OBI:0000891": "A cytometry assay which measures the degree to which input cells are replicating.",
        "OBI:0000893": "An assay, based on the PCR, that amplifies and simultaneously quantifies a specific DNA molecule based on the use of complementary probes/primers. It enables both detection and quantification (as absolute number of copies or relative amount when normalized to DNA input or additional normalizing genes) of one or more specific sequences in a DNA sample.",
        "OBI:0001146": "An assay with the objective to characterize the disposition of two or more material entities to form a complex.",
        "OBI:0001501": "An assay in which a material's fluorescence is determined.",
        "OBI:0001977": "An assay that measures properties of cells.",
        "OBI:0002020": "An assay that identifies epigenetic modifications including histone modifications, open chromatin, and DNA methylation.",
        "OBI:0002039": "An assay to capture the location of open chromatin, DNA-binding proteins, individual nucleosomes and chromatin compaction at nucleotide resolution by Tn5 transposase insertion.",
        "OBI:0002082": "An assay that detects expression of a reporter gene that was inserted under the control of a regulatory sequence of interest.",
        "OBI:0002948": null,
        "OBI:0002955": null,
        "OBI:0002956": null,
        "OBI:0002957": null,
        "OBI:0002958": null,
        "OBI:0002968": null,
        "OBI:0002969": null,
        "OBI:0002970": null,
        "OBI:0200198": "Tandem mass spectrometry is a data transformation that uses two or more analyzers separated by a region in which ions can be induced to fragment by transfer of energy (frequently by collision with other molecules)."
      }
    },
    "metric": -27,
    "name": "list of any assay terms in assay_type.tsv NOT associated with files",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 1,
    "comment": "4 / 4",
    "supplement": {},
    "metric": -28,
    "name": "list of any format terms in file_format.tsv NOT associated with files",
    "description": "",
    "detail": "",
    "principle": ""
  },
  {
    "value": 1,
    "comment": "5 / 5",
    "supplement": {},
    "metric": -29,
    "name": "list of any data type terms in data_type.tsv NOT associated with files",
    "description": "",
    "detail": "",
    "principle": ""
  }
]
```
