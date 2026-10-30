# B2B Vendor-Managed Inventory (VMI) & Consignment Ledger Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

Vendor Managed Inventory (VMI) consignment sell-through ledger matching, shrinkage loss allowance, and title transfer invoice trigger. Built for GenPark (https://www.genpark.ai).

## Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## MCP Tools Exposed
- `reconcile_vmi_consignment_consumption`: Match buyer consumption telemetry against consignment stock on hand to trigger automated self-billing title transfer invoices.
- `compute_consignment_safety_replenishment_trigger`: Calculate automated replenishment purchase order quantity when consignment stock breaches min-max buffer.

## Installation & Usage
```bash
python -m genpark_agentic_commerce_b2b_vmi_consignment_inventory_skill.server --test
```
