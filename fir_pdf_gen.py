from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from fpdf import FPDF
from pydantic import BaseModel
import os
import uuid
import httpx

router = APIRouter()

class FIRPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "FIRST INFORMATION REPORT (FIR)", align="C", ln=True)
        self.ln(10)

def generate_fir_pdf(data: dict) -> str:
    pdf = FIRPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # Add content
    pdf.cell(0, 10, f"Book No.: {data['book_no']}", ln=True)
    pdf.cell(0, 10, f"Form No.: {data['form_no']}", ln=True)
    pdf.cell(0, 10, f"Police Station: {data['police_station']}", ln=True)
    pdf.cell(0, 10, f"District: {data['district']}", ln=True)
    pdf.cell(0, 10, f"Date and Hour of Occurrence: {data['date_hour_occurrence']}", ln=True)
    pdf.cell(0, 10, f"Date and Hour when Reported: {data['date_hour_reported']}", ln=True)
    pdf.cell(0, 10, f"Name and Residence of Informer/Complainant: {data['informer_name']}", ln=True)
    pdf.multi_cell(0, 10, f"Brief Description of Offense (with Section) and Property Carried Off (if any): {data['description_offense']}")
    pdf.cell(0, 10, f"Place of Occurrence and Distance/Direction from Police Station: {data['place_occurrence']}", ln=True)
    pdf.cell(0, 10, f"Name and Address of the Criminal: {data['criminal_name']}", ln=True)
    pdf.multi_cell(0, 10, f"Steps Taken Regarding Investigation/Explanation of Delay: {data['investigation_steps']}")
    pdf.cell(0, 10, f"Date and Time of Dispatch from Police Station: {data['dispatch_time']}", ln=True)
    pdf.cell(0, 10, f"Signature of Writer: ..............................", ln=True)
    
    # Save PDF
    output_dir = "fir_reports"
    os.makedirs(output_dir, exist_ok=True)
    file_name = f"FIR_Report_{uuid.uuid4().hex}.pdf"
    file_path = os.path.join(output_dir, file_name)
    pdf.output(file_path)
    return file_path

class FIRDetails(BaseModel):
    book_no: str
    form_no: str
    police_station: str
    district: str
    date_hour_occurrence: str
    date_hour_reported: str
    informer_name: str
    description_offense: str
    place_occurrence: str
    criminal_name: str
    investigation_steps: str
    dispatch_time: str

@router.post("/")
async def generate_fir(details: FIRDetails):
    try:
        file_path = generate_fir_pdf(details.dict())
        return {
            "message": "FIR PDF generated successfully!",
            "download_url": f"http://192.168.123.233:8000/generate-fir/download/{os.path.basename(file_path)}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{file_name}")
async def download_file(file_name: str):
    file_path = os.path.join("fir_reports", file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="application/pdf", filename=file_name)

async def get_lawgpt_response(description_offense: str) -> str:
    """
    Sends the description_offense to an external service and retrieves the response.
    """
    url = "http://192.168.123.233:8000/lawgpt/chat"  # Replace with the actual URL
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json={"description_offense": description_offense})
            response.raise_for_status()  # Raise an error for HTTP codes >= 400
            data = response.json()
            return data.get("response", description_offense)  # Use original if no response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get response from LawGPT: {str(e)}")

@router.post("/")
async def generate_fir(details: FIRDetails):
    try:
        # Get response from LawGPT for description_offense
        updated_description = await get_lawgpt_response(details.description_offense)
        
        # Replace the description_offense with the processed response
        details.description_offense = updated_description

        # Generate PDF with the updated description
        file_path = generate_fir_pdf(details.dict())
        
        return {
            "message": "FIR PDF generated successfully!",
            "download_url": f"http://192.168.123.233:8000/generate-fir/download/{os.path.basename(file_path)}"
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))