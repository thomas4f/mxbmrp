# shader_generator.py

from pathlib import Path

REPLACEMENTS = {
    " ": "__Space",
    "!": "__Exclam",
    '"': "__Quote",
    "#": "__Pound",
    "$": "__Dollar",
    "%": "__Percent",
    "&": "__And",
    "'": "__sQuote",
    "(": "__rBrac_O",
    ")": "__rBrac_C",
    "*": "__Asterisk",
    "+": "__Plus",
    ",": "__Comma",
    "-": "__Minus",
    ".": "__Dot",
    "/": "__Slash",
    "0": "__0",
    "1": "__1",
    "2": "__2",
    "3": "__3",
    "4": "__4",
    "5": "__5",
    "6": "__6",
    "7": "__7",
    "8": "__8",
    "9": "__9",
    ":": "__Colon",
    ";": "__sColon",
    "<": "__Less",
    "=": "__Equals",
    ">": "__Greater",
    "?": "__Question",
    "@": "__at",
    "A": "__A",
    "B": "__B",
    "C": "__C",
    "D": "__D",
    "E": "__E",
    "F": "__F",
    "G": "__G",
    "H": "__H",
    "I": "__I",
    "J": "__J",
    "K": "__K",
    "L": "__L",
    "M": "__M",
    "N": "__N",
    "O": "__O",
    "P": "__P",
    "Q": "__Q",
    "R": "__R",
    "S": "__S",
    "T": "__T",
    "U": "__U",
    "V": "__V",
    "W": "__W",
    "X": "__X",
    "Y": "__Y",
    "Z": "__Z",
    "[": "__sBrac_O",
    "\\": "__Backslash",
    "]": "__sBrac_C",
    "^": "__Caret",
    "_": "__Underscore",
    "{": "__cBrac_O",
    "|": "__vBar",
    "}": "__cBrac_C",
    "~": "__Tilde",
    "a": "__a",
    "b": "__b",
    "c": "__c",
    "d": "__d",
    "e": "__e",
    "f": "__f",
    "g": "__g",
    "h": "__h",
    "i": "__i",
    "j": "__j",
    "k": "__k",
    "l": "__l",
    "m": "__m",
    "n": "__n",
    "o": "__o",
    "p": "__p",
    "q": "__q",
    "r": "__r",
    "s": "__s",
    "t": "__t",
    "u": "__u",
    "v": "__v",
    "w": "__w",
    "x": "__x",
    "y": "__y",
    "z": "__z",
}


def format_content(content_tpl, mem_info, max_len, verbose):
    # Helper function to truncate strings
    def truncate(text, max_length):
        if not isinstance(text, str):
            text = str(text)
        return text if len(text) <= max_length else text[: max_length - 4] + " ..."

    # Format and output the memory information with truncation
    tpl_data = {
        "Bike": truncate(mem_info.get("bike_name") or "None", max_len),
        "Track": truncate(mem_info.get("track_name") or "None", max_len),
        "Server": truncate(
            mem_info.get("local_server_name") or mem_info.get("server_name") or "None",
            max_len,
        ),
        "Password": truncate(
            mem_info.get("local_server_password")
            or mem_info.get("server_password")
            or "None",
            max_len,
        ),
    }

    formatted_content = content_tpl.format(**tpl_data)

    if verbose:
        print(formatted_content)

    return formatted_content


def gen_shader(shader_src_path, shader_dest_path, formatted_content, layer_src_path, verbose):
    # Generate final shader
    if verbose:
        print("Generating shader")
    shader_code = []
    
    # Path in shader must use forward slashes
    posix_layer_src_path = Path(layer_src_path).as_posix()

    # Generate code
    for idx, line in enumerate(formatted_content.splitlines()):
        replaced = [REPLACEMENTS.get(char, "__Question") for char in line]
        array_size = len(replaced)
        array_elements = ", ".join(replaced)
        shader_code.append(
            f"    int textContent{idx}[{array_size}] = {{ {array_elements} }};"
        )
        shader_code.append(
            f"    DrawText_String(float2(basePos.x, currentY), TextSize, 1, texCoord, textContent{idx}, {array_size}, alpha);"
        )
        shader_code.append("    currentY += lineOffset;")
    final_shader = shader_src_path.replace("{{ generated_code }}", "\n".join(shader_code))
    final_shader = final_shader.replace("{{ layer_src_path }}", f'"{posix_layer_src_path}"')

    # Write shader to disk
    if verbose:
        print(f"Writing shader: {shader_dest_path}")
    with open(shader_dest_path, "w") as f:
        f.write(final_shader)
