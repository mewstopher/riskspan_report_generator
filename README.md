# RiskSpan Report Generator
This project is for generating the reports for the RiskSpan skills assessment

## how to use
This project is build to use the input ```.xlsx``` file that was provided (can also be found in the ```/data/``` dir)
1. build project by running: ```make build```
2. use any of the `cli.py commands`.
Ex. Creating the LTV output:
```
$ riskspan_report_generator ltv-report --data location/RiskSpanSkillsAssessment.xlsx --sheetname Data
```

## results
Find results in the ```data/``` directory. The ```.xlsx``` file is the input (unchanged) data.
