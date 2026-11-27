"""Export generated AI content into downloadable files."""

from io import BytesIO
from docx import Document


def export_to_txt(content):
    """Convert generated content into TXT file bytes."""

    if isinstance(content, dict):
        text = "\n\n".join(
            f"{key.replace('_', ' ').title()}\n{value}"
            for key, value in content.items()
        )
    else:
        text = str(content)

    return text.encode("utf-8")


def export_to_docx(content, title="AI Generated Content"):
    """Convert generated content into a DOCX document."""

    document = Document()
    document.add_heading(title, level=1)

    if isinstance(content, dict):
        for section, text in content.items():
            document.add_heading(
                section.replace("_", " ").title(),
                level=2
            )
            document.add_paragraph(str(text))
    else:
        document.add_paragraph(str(content))

    file_buffer = BytesIO()
    document.save(file_buffer)
    file_buffer.seek(0)

    return file_buffer.getvalue()