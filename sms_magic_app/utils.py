from .database import DB


async def get_next_sequence_id(table: str) -> int:
    """Get next id sequence for the given table.

    Args:
        table: table name for which we want to generate next sequence.

    Returns:
        This will return next sequence for new record.
    """
    return max([record["id"] for record in DB[table]]) + 1
