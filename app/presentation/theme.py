from rich.theme import Theme

LIST_MARKER = '•' # Used to mark existence of resource in list
TAB = ' ' * 4 # Define tab width in presentations

ICON = {
    'manuscript': '✎',  #📝',
    'recording': '▶',  #🔊',
    'resource': '✚',  #📎',
    'missing_file': '✘'
}

# Suggestions for icons to use:
# ✎ ✍ ♪ ♫ ▸ ▶ ≡ ¶  ✚ ❑ ❏ ❦ ➕ ▤ ▢
# 📄 📕 📝 🔊 🎧 🎙️ ▶ 📎 📁 📚


custom_theme = Theme ({
    'info': 'italic',
    'title': 'bold',
    'sermon_code': 'bold',
    'key': 'bold yellow',
    'code': 'dim italic',
    'notes': 'dim',
    'alert': 'red bold',
    'link_style': 'dim'    # Add this theme to links like this: [link=http...][link_style]link_text[/link_style][/link]
})


#  Styles:
#  "bold" or "b" for bold text.
#  "blink" for text that flashes (use this one sparingly).
#  "blink2" for text that flashes rapidly (not supported by most terminals).
#  "conceal" for concealed text (not supported by most terminals).
#  "italic" or "i" for italic text (not supported on Windows).
#  "reverse" or "r" for text with foreground and background colors reversed.
#  "strike" or "s" for text with a line through it.
#  "underline" or "u" for underlined text.
#  "underline2" or "uu" for doubly underlined text.
#  "frame" for framed text.
#  "encircle" for encircled text.
#  "overline" or "o" for overlined text.
#  
#  







