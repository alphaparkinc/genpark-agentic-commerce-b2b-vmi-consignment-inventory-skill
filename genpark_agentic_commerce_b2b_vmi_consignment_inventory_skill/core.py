# -*- coding: utf-8 -*-
"""B2B VMI Consignment Ledger Engine for GenPark Agentic Commerce."""
import json
from typing import Dict, Any

class B2BVMIConsignmentLedgerEngine:
    @staticmethod
    def reconcile_vmi_consignment_consumption(consignment_stock_on_hand: int, consumed_units: int, unit_contract_price_usd: float, allowed_shrinkage_pct: float = 0.5) -> Dict[str, Any]:
        billable_units = min(consignment_stock_on_hand, consumed_units)
        remaining_stock = consignment_stock_on_hand - billable_units
        invoice_total_usd = round(billable_units * unit_contract_price_usd, 2)
        
        return {
            "initial_consignment_stock": consignment_stock_on_hand,
            "reconciled_consumption_units": billable_units,
            "remaining_unbilled_consignment_stock": remaining_stock,
            "title_transfer_invoice_usd": invoice_total_usd,
            "accounting_directive": f"Generate AP debit memo for {invoice_total_usd} USD upon title transfer confirmation."
        }

    @staticmethod
    def compute_consignment_safety_replenishment_trigger(current_stock: int, min_buffer: int, max_capacity: int) -> Dict[str, Any]:
        needs_replenishment = current_stock <= min_buffer
        reorder_qty = max(0, max_capacity - current_stock) if needs_replenishment else 0
        return {
            "current_consignment_stock": current_stock,
            "minimum_buffer_threshold": min_buffer,
            "replenishment_triggered": needs_replenishment,
            "recommended_dispatch_units": reorder_qty,
            "vmi_status": "AUTO_DISPATCH_ORDER_GENERATED" if needs_replenishment else "OPTIMAL_STOCK_BUFFER"
        }
