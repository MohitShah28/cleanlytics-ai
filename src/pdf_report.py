from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from xml.sax.saxutils import escape


def _safe_text(value, max_len=180):
    text = "" if value is None else str(value)
    text = text.replace("\n", " ").replace("\r", " ").strip()
    if len(text) > max_len:
        text = text[: max_len - 3] + "..."
    return escape(text)


def _chunk_rows(rows, size):
    for i in range(0, len(rows), size):
        yield rows[i:i + size]


def generate_pdf_report(
    file_path,
    dataset_name,
    rows,
    columns,
    missing_values,
    duplicate_rows,
    quality_score,
    schema_rows=None,
    iqr_outliers=None,
    zscore_outliers=None,
    iso_outliers=None,
    cleaning_summary=None,
    cleaned_file_count=0,
    backup_file_count=0
):

    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading2"],
            fontSize=13,
            textColor=colors.HexColor("#1f4e79"),
            spaceAfter=8,
            spaceBefore=8
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallMuted",
            parent=styles["BodyText"],
            fontSize=9,
            textColor=colors.HexColor("#666666")
        )
    )

    elements = []

    # Header band
    header = Table(
        [[Paragraph("<b>Cleanlytics AI - Executive Data Report</b>", styles["Title"])]],
        colWidths=[doc.width]
    )
    header.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eaf2fb")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#1f4e79")),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])
    )
    elements.append(header)
    elements.append(Spacer(1, 8))
    elements.append(Paragraph("Client-ready snapshot of dataset health and detected risks.", styles["SmallMuted"]))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#d9d9d9")))
    elements.append(Spacer(1, 10))

    # Summary section
    elements.append(Paragraph("Data Profiling Summary", styles["SectionTitle"]))

    if quality_score >= 90:
        quality_band = "Excellent"
        quality_color = colors.HexColor("#dff3e3")
    elif quality_score >= 70:
        quality_band = "Moderate"
        quality_color = colors.HexColor("#fff2cc")
    else:
        quality_band = "Poor"
        quality_color = colors.HexColor("#f8d7da")

    summary_data = [
        ["Dataset", _safe_text(dataset_name, 120)],
        ["Rows", f"{rows:,}"],
        ["Columns", f"{columns:,}"],
        ["Missing Values", f"{missing_values:,}"],
        ["Duplicate Rows", f"{duplicate_rows:,}"],
        ["Quality Score", f"{quality_score}/100 ({quality_band})"],
    ]

    summary_table = Table(summary_data, colWidths=[doc.width * 0.33, doc.width * 0.67])
    summary_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f5f7fa")),
            ("BACKGROUND", (1, 5), (1, 5), quality_color),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1a1a1a")),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d9d9d9")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )
    elements.append(summary_table)
    elements.append(Spacer(1, 14))

    # -----------------------------
    # BEFORE VS AFTER CLEANING
    # -----------------------------
    elements.append(Paragraph("Before vs After Cleaning", styles["SectionTitle"]))

    if cleaning_summary:
        comparison_rows = [
            ["Metric", "Before Cleaning", "After Cleaning", "Change"],
            [
                "Rows",
                str(cleaning_summary.get("before_rows", "")),
                str(cleaning_summary.get("after_rows", "")),
                str(cleaning_summary.get("after_rows", 0) - cleaning_summary.get("before_rows", 0))
            ],
            [
                "Missing Values",
                str(cleaning_summary.get("before_missing", "")),
                str(cleaning_summary.get("after_missing", "")),
                str(cleaning_summary.get("after_missing", 0) - cleaning_summary.get("before_missing", 0))
            ],
            [
                "Duplicate Rows",
                str(cleaning_summary.get("before_duplicates", "")),
                str(cleaning_summary.get("after_duplicates", "")),
                str(cleaning_summary.get("after_duplicates", 0) - cleaning_summary.get("before_duplicates", 0))
            ],
            [
                "Quality Score",
                f"{cleaning_summary.get('before_quality_score', 0)}/100",
                f"{cleaning_summary.get('after_quality_score', 0)}/100",
                str(round(
                    cleaning_summary.get("after_quality_score", 0) -
                    cleaning_summary.get("before_quality_score", 0), 2
                ))
            ],
        ]

        comparison_table = Table(
            comparison_rows,
            colWidths=[
                doc.width * 0.25,
                doc.width * 0.25,
                doc.width * 0.25,
                doc.width * 0.25,
            ],
            repeatRows=1
        )
        comparison_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2f4858")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d9d9d9")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ])
        )
        elements.append(comparison_table)
    else:
        elements.append(Paragraph("No cleaning run found yet. Run Data Cleaning to include this section.", styles["BodyText"]))

    elements.append(Spacer(1, 14))

    # -----------------------------
    # AI SCHEMA REPORT SECTION
    # -----------------------------
    elements.append(Paragraph("AI Schema Report", styles["SectionTitle"]))

    if schema_rows:
        schema_header = ["Column", "Current Type", "Suggested Type", "Confidence", "Reason"]
        total_schema_rows = len(schema_rows)
        elements.append(Paragraph(f"Columns analyzed: {total_schema_rows}", styles["SmallMuted"]))
        elements.append(Spacer(1, 6))

        # Auto-paginate schema table in chunks for large datasets.
        schema_chunk_size = 45
        for chunk_index, schema_chunk in enumerate(_chunk_rows(schema_rows, schema_chunk_size)):
            schema_table_rows = [schema_header]
            for row in schema_chunk:
                schema_table_rows.append([
                    Paragraph(_safe_text(row.get("Column", ""), 50), styles["BodyText"]),
                    Paragraph(_safe_text(row.get("Current Data Type", ""), 40), styles["BodyText"]),
                    Paragraph(_safe_text(row.get("AI Suggested Type", ""), 40), styles["BodyText"]),
                    Paragraph(_safe_text(row.get("Confidence", ""), 30), styles["BodyText"]),
                    Paragraph(_safe_text(row.get("Reason", ""), 180), styles["BodyText"]),
                ])

            # Slightly smaller font when table gets large.
            schema_font_size = 8 if total_schema_rows > 60 else 9

            schema_table = Table(
                schema_table_rows,
                colWidths=[
                    doc.width * 0.18,
                    doc.width * 0.15,
                    doc.width * 0.15,
                    doc.width * 0.12,
                    doc.width * 0.40,
                ],
                repeatRows=1
            )
            schema_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), schema_font_size),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cfd8e3")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fbff")]),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ])
            )
            elements.append(schema_table)
            elements.append(Spacer(1, 8))

            if chunk_index < (total_schema_rows - 1) // schema_chunk_size:
                elements.append(PageBreak())
                elements.append(Paragraph("AI Schema Report (continued)", styles["SectionTitle"]))
    else:
        elements.append(Paragraph("No schema details available.", styles["BodyText"]))

    elements.append(Spacer(1, 14))

    # -----------------------------
    # OUTLIER DETECTION SECTION
    # -----------------------------
    elements.append(Paragraph("Outlier Detection Summary", styles["SectionTitle"]))

    def add_outlier_block(title, rows_data):
        elements.append(Paragraph(f"<b>{title}</b>", styles["BodyText"]))
        if rows_data:
            total_rows = len(rows_data)
            header = list(rows_data[0].keys())[:6]
            elements.append(Paragraph(f"Detected records: {total_rows}", styles["SmallMuted"]))

            table_rows = [header]
            preview_limit = 60
            for row in rows_data[:preview_limit]:
                table_rows.append([_safe_text(row.get(k, ""), 80) for k in header])

            # If many columns exist, fallback to paragraph list to avoid overflow.
            if len(header) > 5:
                for row in rows_data[:20]:
                    parts = [f"{k}: {_safe_text(row.get(k, ''), 90)}" for k in header]
                    elements.append(Paragraph(" | ".join(parts), styles["BodyText"]))
            else:
                widths = [doc.width / len(header)] * len(header)
                outlier_table = Table(table_rows, colWidths=widths, repeatRows=1)
                outlier_table.setStyle(
                    TableStyle([
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#355c7d")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 9),
                        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d9d9d9")),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f7fb")]),
                        ("LEFTPADDING", (0, 0), (-1, -1), 5),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                        ("TOPPADDING", (0, 0), (-1, -1), 4),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ])
                )
                elements.append(outlier_table)
                if total_rows > preview_limit:
                    elements.append(
                        Paragraph(
                            f"Showing first {preview_limit} rows out of {total_rows}.",
                            styles["SmallMuted"]
                        )
                    )
        else:
            elements.append(Paragraph("No major outliers detected.", styles["BodyText"]))
        elements.append(Spacer(1, 8))

    add_outlier_block("IQR Method", iqr_outliers)
    add_outlier_block("Z-Score Method", zscore_outliers)
    add_outlier_block("Isolation Forest Method", iso_outliers)

    doc.build(elements)
