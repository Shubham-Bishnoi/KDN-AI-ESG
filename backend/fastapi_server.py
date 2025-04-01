from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import subprocess
from zipfile import ZipFile

app = FastAPI()

#  Enable CORS so frontend (localhost:3000) can access this backend (localhost:5050)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify ["http://localhost:3000"] for stricter control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Paths
REPORTS_DIR = "data/reports"
TNFD_GENERATOR_SCRIPT = "dashboard/reports/generate_tnfd_report.py"

#  Endpoint to generate ESG report
@app.get("/generate-report/{report_type}")
def generate_report(report_type: str):
    try:
        print(f" API Triggered: /generate-report/{report_type}")

        # Only run TNFD PDF generation (multi_org_report.json is assumed pre-generated)
        result = subprocess.run(
            ["python", TNFD_GENERATOR_SCRIPT],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(" TNFD Generator stderr:\n", result.stderr)
            raise HTTPException(status_code=500, detail="Report generation failed")

        print(" TNFD report generation complete.")
        return {"message": f"{report_type.capitalize()} report generated successfully."}

    except Exception as e:
        print(" Report generation exception:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to download report for a company
@app.get("/download-report/{company_name}")
def download_report_by_company(company_name: str):
    try:
        safe_name = company_name.replace(" ", "_").lower()
        file_path = os.path.join(REPORTS_DIR, f"{safe_name}.pdf")

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"No report found for company: {company_name}")

        print(f"📦 Sending: {file_path}")
        return FileResponse(file_path, filename=f"{safe_name}_report.pdf", media_type="application/pdf")
    except Exception as e:
        print(f" Error sending report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

#  Download all PDFs as a zip
@app.get("/download-all-reports")
def download_all_reports():
    try:
        zip_path = os.path.join(REPORTS_DIR, "All_Company_ESG_Reports.zip")

        with ZipFile(zip_path, "w") as zipf:
            for file in os.listdir(REPORTS_DIR):
                if file.endswith(".pdf"):
                    zipf.write(os.path.join(REPORTS_DIR, file), arcname=file)

        print(f" Sending ZIP: {zip_path}")
        return FileResponse(zip_path, filename="All_Company_ESG_Reports.zip", media_type="application/zip")
    except Exception as e:
        print(" ZIP creation error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
