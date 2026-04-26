# Budget Variance Agent MVP Scope

## Input Fields

The v1.1 MVP expects structured budget vs actual data with the following fields:

- `period`
- `department`
- `account`
- `budget_amount`
- `actual_amount`
- `variance_amount`
- `variance_rate`
- `business_driver`
- `remark`

## Output Report Sections

The generated management report should include:

- 总体结论
- 收入预算执行情况
- 成本费用预算执行情况
- 重大偏差项目
- 异常归因
- 对利润和现金流的影响
- 管理建议
- 下月关注事项

## v1.1 Non-Goals

The v1.1 MVP does not:

- 不接真实 ERP
- 不做复杂预测
- 不接真实银行流水
- 不做审计意见
- 不替代人工财务判断

## MVP Boundary

The agent should provide structured analysis and management insight based on user-provided sample data. It should not claim authoritative audit, accounting, tax, treasury, or legal conclusions.
