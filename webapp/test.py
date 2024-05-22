def coloured_square(hex_string):
    """
    Returns a coloured square that you can print to a terminal.
    """
    hex_string = hex_string.strip("#")
    assert len(hex_string) == 6
    red = int(hex_string[:2], 16)
    green = int(hex_string[2:4], 16)
    blue = int(hex_string[4:6], 16)

    apple = 'label'

    return f"{apple} \033[48:2::{red}:{green}:{blue}m \033[49m"

print(coloured_square('#ec0909'))