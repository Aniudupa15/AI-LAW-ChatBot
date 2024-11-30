import json

def generate_fir(fir_details):
  fir_template = f"""
  Book No.: {fir_details.get("book_no", "N/A")}

  FORM NO. 24.5 (1)
  FIRST INFORMATION REPORT

  First Information of a Cognizable Crime Reported under Section 154, Criminal Penal Code

  Police Station: {fir_details.get("police_station", "N/A")}
  District: {fir_details.get("district", "N/A")}
  FIR No.: {fir_details.get("fir_no", "N/A")}

  Date and hour of Occurrence: {fir_details.get("date_hour_occurrence", "N/A")}
  Date and hour when reported: {fir_details.get("date_hour_reported", "N/A")}
  
  Name and residence of informer and complainant: {fir_details.get("informer_complainant", "N/A")}
  Brief description of offence (with section) and of property carried off, if any:
  {fir_details.get("offence_description", "N/A")}

  Place of occurrence: {fir_details.get("place_occurrence", "N/A")}
  Distance and direction from the Police Station: {fir_details.get("distance_direction_ps", "N/A")}
  
  Name & Address of the Criminal: {fir_details.get("criminal_details", "N/A")}
  
  Steps taken regarding investigation explanation of delay in reporting information:
  {fir_details.get("investigation_steps", "N/A")}
  Explanation of delay in reporting information: {fir_details.get("delay_explanation", "N/A")}

  Date and Time of dispatch from Police Station: {fir_details.get("dispatch_time", "N/A")}
  
  Signatures:
      Informer Signature/Thumb Impression: {fir_details.get("informer_signature", "N/A")}
      Writer of FIR Signature: {fir_details.get("writer_signature", "N/A")}
  
  Designation: {fir_details.get("designation", "N/A")}
  """
  
  return json.dumps({"FIR": fir_template.strip()}, indent=4)



# HOW TO SEND THE DATA -- FOR ANIRUDHA

# fir_data = {
#     "book_no": "123",
#     "police_station": "City Police Station",
#     "district": "Central District",
#     "fir_no": "456",
#     "date_hour_occurrence": "2024-11-30 14:00",
#     "date_hour_reported": "2024-11-30 15:00",
#     "informer_complainant": "John Doe, 123 Elm Street",
#     "offence_description": "Burglary under Section 457 IPC",
#     "place_occurrence": "123 Elm Street",
#     "distance_direction_ps": "2 km North",
#     "criminal_details": "Unknown",
#     "investigation_steps": "Site inspection, evidence collection",
#     "delay_explanation": "Immediate reporting",
#     "dispatch_time": "2024-11-30 16:00",
#     "informer_signature": "John Doe",
#     "writer_signature": "Officer Smith",
#     "designation": "Inspector"
# }

# filled_fir = generate_fir(fir_data)
# print(filled_fir)
