"""Initialize and create architecture decision records (ADRs)."""

import jinja2
import logging
import pathlib
from datetime import date
from toolit import tool

logger = logging.getLogger(__name__)

BASE_PATH = pathlib.Path.cwd() / "architecture_decision_records"
TEMPLATE_PATH = pathlib.Path(__file__).parent


def _today() -> str:
    return date.today().isoformat()


def _create_adr_filename(name: str, ordinal: int) -> str:
    safe = "-".join(name.lower().split())
    return f"{ordinal:04d}-{safe}.md"


def _next_ordinal() -> int:
    if not BASE_PATH.exists():
        return 1

    ordinals = []
    for p in BASE_PATH.glob("*.md"):
        prefix = p.stem.split("-")[0]
        if prefix.isdigit():
            ordinals.append(int(prefix))

    return max(ordinals) + 1 if ordinals else 1

@tool
def adr_init() -> None:
    """Initialize the architecture decision records (ADRs) directory and create the initial ADR."""
    BASE_PATH.mkdir(exist_ok=True)

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_PATH),
        autoescape=True,
    )

    template = env.get_template("initial_adr.jinja2")

    ordinal = 1
    filename = _create_adr_filename("record-architecture-decisions", ordinal)

    content = template.render(
        ordinal=ordinal,
        title="Record Architecture Decisions",
        date=_today(),
    )

    (BASE_PATH / filename).write_text(content, encoding="utf-8")
    logger.info(f"Initialized ADR directory and created initial ADR: {filename}")

@tool
def adr_new(name: str) -> None:
    """Create a new architecture decision record (ADR) with the given name."""
    BASE_PATH.mkdir(exist_ok=True)

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_PATH),
        autoescape=True,
    )

    template = env.get_template("new_adr.jinja2")

    ordinal = _next_ordinal()
    filename = _create_adr_filename(name, ordinal)

    content = template.render(
        ordinal=ordinal,
        title=name.title(),
        date=_today(),
    )
    output_path = BASE_PATH / filename
    output_path.write_text(content, encoding="utf-8")
    logger.info(f"Created new ADR: {output_path}")
