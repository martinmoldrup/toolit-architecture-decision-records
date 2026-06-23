"""Initialize and create architecture decision records (ADRs)."""

import jinja2
import logging
import pathlib
from datetime import date
from toolit import tool
import typer 

logger = logging.getLogger(__name__)

BASE_PATH = pathlib.Path.cwd() / "architecture_decision_records"
TEMPLATE_PATH = pathlib.Path(__file__).parent
FILENAME_NEW_ADR_TEMPLATE = "new_adr.jinja2"
FILENAME_INITIAL_ADR_TEMPLATE = "initial_adr.jinja2"

def _today() -> str:
    return date.today().isoformat()


def _create_adr_filename(name: str, ordinal: int) -> str:
    safe = "-".join(name.lower().split())
    return f"{ordinal:03d}-{safe}.md"


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

    template = env.get_template(FILENAME_INITIAL_ADR_TEMPLATE)

    ordinal = 1
    filename = _create_adr_filename("record-architecture-decisions", ordinal)

    content = template.render(
        ordinal=ordinal,
        title="Record Architecture Decisions",
        date=_today(),
    )

    output_path = BASE_PATH / filename
    if output_path.exists():
        logger.warning(f"Initial ADR already exists: {output_path}.")
        confirm = typer.confirm("Do you want to overwrite it?")
        if not confirm:
            logger.info("Aborting initial ADR creation.")
            return
    output_path.write_text(content, encoding="utf-8")
    logger.info(f"Initialized ADR directory and created initial ADR: {filename}")

@tool
def adr_new(name: str, insert_at: int | None = None) -> None:  
    """Create a new architecture decision record (ADR) with the given name."""
    BASE_PATH.mkdir(exist_ok=True)

    ordinal = _create_ordinal(insert_at)

    # Render new ADR  
    env = jinja2.Environment(  
        loader=jinja2.FileSystemLoader(TEMPLATE_PATH),  
        autoescape=True,  
    )  
    template = env.get_template(FILENAME_NEW_ADR_TEMPLATE)  
  
    filename = _create_adr_filename(name, ordinal)  
    content = template.render(  
        ordinal=ordinal,  
        title=name.title(),  
        date=_today(),  
    )

    output_path = BASE_PATH / filename
    output_path.write_text(content, encoding="utf-8")
    logger.info(f"Created new ADR: {output_path}")

def _shift_adrs_upward(insert_at_ordinal: int) -> None:
    # confirm if the ordinal exists, if not, no need to shift
    existing_ordinals = [int(p.stem.split("-")[0]) for p in BASE_PATH.glob("*.md") if p.stem.split("-")[0].isdigit()]
    if insert_at_ordinal not in existing_ordinals:
        logger.warning(f"Ordinal {insert_at_ordinal} does not exist. No ADRs will be shifted.")
        return
    if max(existing_ordinals) < insert_at_ordinal:
        logger.warning(f"Ordinal {insert_at_ordinal} is greater than the highest existing ordinal. No ADRs will be shifted.")
        return
    for p in sorted(BASE_PATH.glob("*.md"), reverse=True):  
        prefix = p.stem.split("-")[0]  
        if prefix.isdigit():  
            current = int(prefix)  
            if current >= insert_at_ordinal:  
                new_name = _create_adr_filename(  
                        "-".join(p.stem.split("-")[1:]),  
                        current + 1  
                    )  
                p.rename(BASE_PATH / new_name)

def _create_ordinal(insert_at_ordinal: int | None) -> int:
    # Determine target ordinal  
    if insert_at_ordinal is None:  
        return _next_ordinal()  
    # Shift later ADRs upward  
    _shift_adrs_upward(insert_at_ordinal)
    return insert_at_ordinal
