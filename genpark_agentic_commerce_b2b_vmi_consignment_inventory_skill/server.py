# -*- coding: utf-8 -*-
"""MCP Server for B2B Vendor-Managed Inventory (VMI) & Consignment Ledger Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import B2BVMIConsignmentLedgerEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "reconcile_vmi_consignment_consumption",
        "description": "Match buyer consumption telemetry against consignment stock on hand to trigger automated self-billing title transfer invoices.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "consignment_stock_on_hand": {
                    "type": "integer"
                },
                "consumed_units": {
                    "type": "integer"
                },
                "unit_contract_price_usd": {
                    "type": "number"
                },
                "allowed_shrinkage_pct": {
                    "type": "number"
                }
            },
            "required": [
                "consignment_stock_on_hand",
                "consumed_units",
                "unit_contract_price_usd"
            ]
        }
    },
    {
        "name": "compute_consignment_safety_replenishment_trigger",
        "description": "Calculate automated replenishment purchase order quantity when consignment stock breaches min-max buffer.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "current_stock": {
                    "type": "integer"
                },
                "min_buffer": {
                    "type": "integer"
                },
                "max_capacity": {
                    "type": "integer"
                }
            },
            "required": [
                "current_stock",
                "min_buffer",
                "max_capacity"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-b2b-vmi-consignment-inventory-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(B2BVMIConsignmentLedgerEngine, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-agentic-commerce-b2b-vmi-consignment-inventory-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
