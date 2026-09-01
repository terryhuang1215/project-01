from __future__ import annotations

import ast
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Calculator App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def read_index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


class CalcRequest(BaseModel):
    expression: str


_ALLOWED_BINOPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.FloorDiv: lambda a, b: a // b,
    ast.Mod: lambda a, b: a % b,
    ast.Pow: lambda a, b: a**b,
}

_ALLOWED_UNARYOPS = {
    ast.UAdd: lambda a: +a,
    ast.USub: lambda a: -a,
}


def _eval_node(node: ast.AST):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_BINOPS:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return _ALLOWED_BINOPS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARYOPS:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return _ALLOWED_UNARYOPS[op_type](operand)
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


@app.api_route("/api/calc", methods=["GET", "POST"])
def calculate(expression: str | None = None, payload: CalcRequest | None = None):
    expr = expression

    if payload is not None:
        expr = payload.expression
    elif expr is None:
        expr = payload.expression if payload else None

    if expr is None:
        raise HTTPException(status_code=400, detail="Expression is required.")

    cleaned = expr.strip()
    if not cleaned:
        raise HTTPException(status_code=400, detail="Expression is required.")

    try:
        parsed = ast.parse(cleaned, mode="eval")
        result = _eval_node(parsed.body)
    except (SyntaxError, ValueError, ZeroDivisionError, OverflowError):
        raise HTTPException(status_code=400, detail="Invalid mathematical expression.")

    return {"expression": cleaned, "result": result}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("calculator:app", host="0.0.0.0", port=8000, reload=False)
