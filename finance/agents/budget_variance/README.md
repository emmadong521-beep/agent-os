# Budget Variance & Business Insight Agent

The Budget Variance Agent helps finance teams analyze budget execution and generate management-ready business insight reports.

## Goals

- Compare budget vs actual data
- Attribute variances to business drivers
- Detect abnormal items and material deviations
- Generate structured management reports
- Support memory writeback in the future for recurring variance patterns, risk signals, and recommended actions

## MVP Flow

1. Ingest structured budget vs actual data.
2. Classify revenue, cost, and expense items.
3. Identify major favorable and unfavorable variances.
4. Attribute variances using business drivers and remarks.
5. Produce a Chinese management report using the report template.

## Related Files

- `scope.md`: MVP input, output, and non-goals
- `sample_output.md`: sample report output
- `../../../templates/budget_variance_report.md`: report template
- `../../../examples/budget_actual_sample.csv`: sample budget vs actual data
