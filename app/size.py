STEP = 1024

KB = STEP
MB = KB * STEP
GB = MB * STEP


def size_to_string(size: int) -> str:
    if size >= GB:
        return f"{round(size / GB, 2)}GB"
    elif size >= MB:
        return f"{round(size / MB, 2)}MB"
    elif size >= KB:
        return f"{round(size / KB, 2)}KB"

    return size
