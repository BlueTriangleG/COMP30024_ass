from .utils import render_board
def move(action, table) -> dict[tuple, tuple]:
    """
    This function is used to move.
    """
    # get the action
    r, q, dr, dq = action
    # get the cell
    cell = table[(r, q)]
    # get the cell state
    p, k = cell
    # remove the cell
    table.pop((r, q))
    # move the cell
    for i in range(k):
        # let r,d go back to 0 when they larger than 6，and let q,d go back to 6 when they smaller than 0
        if r + dr > 6:
            r = r + dr - 7
        elif r + dr < 0:
            r = r + dr + 7
        else:
            r += dr
        if q + dq > 6:
            q = q + dq - 7
        elif q + dq < 0:
            q = q + dq + 7
        else:
            q += dq
        # if the cell is already in the table
        if (r, q) in table:
            origin_k = table[(r, q)][1]
            current_k = origin_k + 1
            if origin_k == 6:
                #if the cell is already 6, delete it
                table.pop((r, q))
            table[(r, q)] = (p, current_k)
        else:
            table[(r, q)] = (p, 1)
    return table
