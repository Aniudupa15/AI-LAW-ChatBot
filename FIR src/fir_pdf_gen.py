from fpdf import FPDF

class FIRPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "FIRST INFORMATION REPORT (FIR)", align="C", ln=True)
        self.ln(10)

def generate_fir_pdf(book_no, form_no, police_station, district, date_hour_occurrence, date_hour_reported, informer_name, description_offense,  place_occurrence, criminal_name, investigation_steps, dispatch_time):
  pdf = FIRPDF()
  pdf.add_page()
  pdf.set_font("Arial", size=11)
  
  # Add content
  pdf.cell(0, 10, f"Book No.: {book_no}", ln=True)
  pdf.cell(0, 10, f"Form No.: {form_no}", ln=True)
  pdf.cell(0, 10, f"Police Station: {police_station}", ln=True)
  pdf.cell(0, 10, f"District: {district}", ln=True)
  pdf.cell(0, 10, f"Date and Hour of Occurrence: {date_hour_occurrence}", ln=True)
  pdf.cell(0, 10, f"Date and Hour when Reported: {date_hour_reported}", ln=True)
  pdf.cell(0, 10, f"Name and Residence of Informer/Complainant: {informer_name}", ln=True)
  pdf.multi_cell(0, 10, f"Brief Description of Offense (with Section) and Property Carried Off (if any): {description_offense}")
  pdf.cell(0, 10, f"Place of Occurrence and Distance/Direction from Police Station: {place_occurrence}", ln=True)
  pdf.cell(0, 10, f"Name and Address of the Criminal: {criminal_name}", ln=True)
  pdf.multi_cell(0, 10, f"Steps Taken Regarding Investigation/Explanation of Delay: {investigation_steps}")
  pdf.cell(0, 10, f"Date and Time of Dispatch from Police Station: {dispatch_time}", ln=True)
  pdf.cell(0, 10, f"Signature of Writer: ..............................", ln=True)
  
  # Save PDF
  pdf.output("FIR_Report.pdf")
  print("FIR PDF generated successfully!")

# Example inputs
if __name__ == "__main__":
  book_no = input("Enter Book No.: ")
  form_no = input("Enter Form No.: ")
  police_station = input("Enter Police Station: ")
  district = input("Enter District: ")
  date_hour_occurrence = input("Enter Date and Hour of Occurrence: ")
  date_hour_reported = input("Enter Date and Hour When Reported: ")
  informer_name = input("Enter Name and Residence of Informer/Complainant: ")
  description_offense = input("Enter Brief Description of Offense: ")
  place_occurrence = input("Enter Place of Occurrence: ")
  criminal_name = input("Enter Name and Address of the Criminal: ")
  investigation_steps = input("Enter Steps Taken Regarding Investigation: ")
  dispatch_time = input("Enter Date and Time of Dispatch: ")
  
  generate_fir_pdf(book_no, form_no, police_station, district, date_hour_occurrence, date_hour_reported, informer_name, description_offense, place_occurrence, criminal_name, investigation_steps, dispatch_time)
