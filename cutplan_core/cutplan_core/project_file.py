"""Saves and loads a Project as a plain JSON file (a ".cutplan" file)."""

import json
from pathlib import Path
from typing import Union

from .design import Design, Kind
from .material import Material
from .part import Part
from .project import Project

PathLike = Union[str, Path]


def save(path: PathLike, project: Project) -> None:
    d = project.design
    m = project.material

    data = {
        "designName": d.name,
        "kind": d.kind.name,
        "parameters": {p.name: p.value for p in d.parameters},
        "material": {
            "sheetWidth": m.sheet_width,
            "sheetHeight": m.sheet_height,
            "kerf": m.kerf,
            "pricePerSheet": m.price_per_sheet,
        },
    }
    if d.kind == Kind.CUSTOM:
        data["parts"] = [
            {"label": p.label, "width": p.width, "height": p.height, "quantity": p.quantity}
            for p in d.build_parts()
        ]

    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")


def load(path: PathLike) -> Project:
    data = json.loads(Path(path).read_text(encoding="utf-8"))

    name = data.get("designName", "Untitled")
    kind = Kind[data.get("kind", "CUSTOM")]
    params = data.get("parameters", {})

    if kind == Kind.BOOKSHELF:
        design = Design.bookshelf(
            name,
            params.get("width", 0),
            params.get("height", 0),
            params.get("depth", 0),
            params.get("thickness", 0),
            int(round(params.get("shelves", 0))),
        )
    elif kind == Kind.BOX:
        design = Design.box(
            name,
            params.get("width", 0),
            params.get("height", 0),
            params.get("depth", 0),
            params.get("thickness", 0),
        )
    else:
        parts = [
            Part(p["label"], p["width"], p["height"], p["quantity"])
            for p in data.get("parts", [])
        ]
        design = Design.custom(name, parts)

    mat = data.get("material", {})
    material = Material(
        mat.get("sheetWidth", 2440),
        mat.get("sheetHeight", 1220),
        mat.get("kerf", 3),
        mat.get("pricePerSheet", 0),
    )
    return Project(design, material)
