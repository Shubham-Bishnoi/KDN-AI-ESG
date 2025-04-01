import json
import os
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

# Paths
REPORT_JSON = "data/multi_org_report.json"
PDF_REPORT_DIR = "data/reports"

# Ensure folder exists
os.makedirs(PDF_REPORT_DIR, exist_ok=True)

# Load data
def load_esg_data():
    if os.path.exists(REPORT_JSON):
        with open(REPORT_JSON, "r") as f:
            return json.load(f)
    return {}

# Save summary chart
def save_summary_chart(company_name, data):
    labels = ['Deforestation', 'Water Pollution', 'Biodiversity Loss']
    values = [
        data["Deforestation Risk"],
        data["Water Pollution Risk"],
        data["Biodiversity Loss Risk"]
    ]
    colors = ['green', 'blue', 'purple']

    plt.figure(figsize=(4, 3))
    plt.bar(labels, values, color=colors)
    plt.title('Environmental Risk Summary')
    plt.ylim(0, 1)
    plt.tight_layout()

    chart_path = os.path.join(PDF_REPORT_DIR, f"{company_name.replace(' ', '_')}_chart.png")
    plt.savefig(chart_path)
    plt.close()
    return chart_path

# Generate one report
def generate_pdf_report(company_name, data):
    filename = os.path.join(PDF_REPORT_DIR, f"{company_name.replace(' ', '_')}.pdf")
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # ✅ Page 1: Company ESG Summary
    story.append(Paragraph("TNFD-Compliant ESG Report", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Company:</b> {company_name}", styles['Normal']))
    story.append(Spacer(1, 12))

    chart_path = save_summary_chart(company_name, data)
    if os.path.exists(chart_path):
        story.append(Image(chart_path, width=300, height=200))
        story.append(Spacer(1, 12))

    story.append(Paragraph(f"<b>Deforestation Risk:</b> {data['Deforestation Risk']:.3f}", styles['Normal']))
    story.append(Paragraph(f"<b>Water Pollution Risk:</b> {data['Water Pollution Risk']:.3f}", styles['Normal']))
    story.append(Paragraph(f"<b>Biodiversity Loss Risk:</b> {data['Biodiversity Loss Risk']:.3f}", styles['Normal']))
    story.append(Paragraph(f"<b>Natural Capital Value:</b> ${data['Natural Capital Value ($)']:,.2f}", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Recommendations:</b>", styles['Heading3']))
    for rec in data["Recommendations"]:
        story.append(Paragraph(f"- {rec}", styles['Normal']))

    #  Page 2: TNFD Guidelines
    story.append(PageBreak())
    story.append(Paragraph("ESG Reporting & TNFD Framework – Guidance for Companies", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "The TNFD (Taskforce on Nature-related Financial Disclosures) is a market-led, "
        "science-based and government-supported initiative. It provides a framework to help organizations "
        "identify, manage and disclose their nature-related dependencies, impacts, risks and opportunities.",
        styles['Normal']
    ))

    bullets = [
        " Market Usability – Easy to integrate with investor reporting.",
        " Science-Based – Grounded in environmental science.",
        " Nature Risk Identification – Focus on risks across Land, Ocean, Freshwater and Atmosphere.",
        " ESG Integration – Works with existing ESG standards like TCFD.",
        " Time Horizons – Covers short- and long-term environmental risk.",
        " Transparency – Helps stakeholders understand nature impact.",
        " Global Relevance – Applicable across industries and regions."
    ]

    for item in bullets:
        story.append(Paragraph(item, styles["Bullet"]))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>How This Report Was Generated:</b>", styles['Heading3']))
    story.append(Paragraph(
        "This AI-generated ESG report uses satellite imagery, biodiversity modeling, water risk analysis, "
        "and carbon valuation techniques aligned with TNFD principles. Models were trained using real-world "
        "land-use data and environmental indicators. Risk values are normalized (0 to 1) for interpretability.",
        styles['Normal']
    ))

    doc.build(story)
    return filename

# Generate all
def generate_tnfd_reports():
    esg_data = load_esg_data()
    if not esg_data:
        print(" No ESG data found.")
        return

    print("📄 Generating TNFD ESG Reports...")
    for company, data in esg_data.items():
        try:
            pdf_file = generate_pdf_report(company, data)
            print(f"✅ {company} Report Saved: {pdf_file}")
        except Exception as e:
            print(f"Failed for {company}: {e}")

# Run
if __name__ == "__main__":
    generate_tnfd_reports()
