"""ADR-0011 memory scope → canonical directory resolver.

Single source of truth for the user / project_shared / project_local →
canonical memory directory mapping. Used by:

- CLI ``mm mem add`` (``cli/memory.py``)
- MCP ``mem_add`` / ``mem_batch_add`` (``server/tools/memory_crud.py``)
- ``mem_consolidate_apply`` summary writes (``server/tools/consolidation.py``)
- ``mm context memory-migrate`` (``cli/context_cmd.py``)

Keeping the helper here (instead of inside ``cli/memory.py`` or
``server/tools/memory_crud.py``) avoids cross-importing CLI deps from
server code (and vice versa) when the same resolution is needed on
both surfaces.
"""

from __future__ import annotations

from pathlib import Path

from memtomem.config import TargetScope


DEFAULT_USER_MEMORY_DIR = Path("~/.memtomem/memories")


class MemoryScopeError(ValueError):
    """Raised when scope → directory resolution cannot proceed.

    Surface-specific wrappers (``click.ClickException`` for the CLI,
    plain string error messages for MCP tool returns) catch and rewrap
    so each layer surfaces user-facing errors in its native vocabulary.
    """


def resolve_memory_scope_dir(
    scope: TargetScope,
    project_root: Path | None,
    user_base: Path = DEFAULT_USER_MEMORY_DIR,
) -> Path:
    """Resolve an ADR-0011 memory scope to its canonical directory.

    Args:
        scope: One of ``user`` / ``project_shared`` / ``project_local``.
        project_root: Required when ``scope`` is a project tier; the
            project root (the grandparent of the
            ``.memtomem/memories[.local]`` entry registered in
            ``IndexingConfig.project_memory_dirs``). Pass ``None`` for
            ``user`` scope.
        user_base: Override for the user-tier base directory. Defaults
            to ``~/.memtomem/memories`` — the historical hardcoded path
            that ``mm mem add`` used pre-ADR-0011.

    Returns:
        The resolved, expanded canonical directory ``Path`` for the
        given scope. The directory may not exist yet; callers create it
        before writing.

    Raises:
        MemoryScopeError: When ``scope`` is a project tier but
            ``project_root`` is ``None``, or when ``scope`` is unknown.
    """
    if scope == "user":
        return user_base.expanduser().resolve()
    if project_root is None:
        raise MemoryScopeError(
            f"scope='{scope}' requires a registered project context "
            "(no project_memory_dirs entry covers the current cwd)."
        )
    if scope == "project_shared":
        return (project_root / ".memtomem" / "memories").resolve()
    if scope == "project_local":
        return (project_root / ".memtomem" / "memories.local").resolve()
    raise MemoryScopeError(f"unsupported memory scope: {scope!r}")
