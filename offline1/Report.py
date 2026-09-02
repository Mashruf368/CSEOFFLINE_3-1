from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def generate_report(all_results):

    doc = SimpleDocTemplate("Weighted_AStar_Report.pdf")

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph("<b>Weighted A* Performance Comparison</b>", styles["Title"])

    elements.append(title)

    elements.append(Paragraph("<br/><br/>", styles["Normal"]))

    table_data = [
        [
            "Puzzle",
            "Weight",
            "Solution Cost",
            "Expanded Nodes"
        ]
    ]

    for puzzle_no, result in enumerate(all_results, start=1):

        best_cost = min(r[1] for r in result)
        best_nodes = min(r[2] for r in result)

        for w, cost, nodes in result:

            cost_text = str(cost)
            node_text = str(nodes)

            if cost == best_cost:
                cost_text = "<b>" + cost_text + "</b>"

            if nodes == best_nodes:
                node_text = "<b>" + node_text + "</b>"

            table_data.append(
                [
                    puzzle_no,
                    w,
                    Paragraph(cost_text, styles["BodyText"]),
                    Paragraph(node_text, styles["BodyText"])
                ]
            )

    table = Table(table_data)

    table.setStyle(TableStyle([

        ('GRID',(0,0),(-1,-1),1,colors.black),

        ('BACKGROUND',(0,0),(-1,0),colors.lightblue),

        ('TEXTCOLOR',(0,0),(-1,0),colors.white),

        ('ALIGN',(0,0),(-1,-1),'CENTER'),

        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),

        ('BOTTOMPADDING',(0,0),(-1,0),12),

        ('BACKGROUND',(0,1),(-1,-1),colors.beige),

        ('FONTSIZE',(0,0),(-1,-1),10)

    ]))

    elements.append(table)

    doc.build(elements)

    print("PDF generated successfully.")