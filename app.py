import streamlit as st
from io import BytesIO
import datetime
import xlsxwriter

# Dropdown options
exPSA_brands = ["Peugeot", "Citroën", "DS", "Opel", "Vauxhall"]
exFCA_brands = ["Fiat", "Jeep", "Chrysler", "Dodge", "RAM", "Alfa Romeo", "Abarth", "Lancia", "Maserati"]

exPSA_agencies = [
    "PSA AT", "PSA BE", "PSA CH", "PSA DE", "PSA ES", "PSA FR", "PSA IT",
    "PSA NL", "PSA PT", "PSA UK", "PSA PL", "PSA TR"
]

exFCA_agencies = [
    "FCA AT", "FCA BE", "FCA CH", "FCA CZ", "FCA DE", "FCA DK", "FCA ES", "FCA FI",
    "FCA FR", "FCA GR", "FCA HU", "FCA IE", "FCA IT", "FCA CENTRAL", "FCA MENA",
    "FCA NL", "FCA NO", "FCA PL", "FCA PT", "FCA RU", "FCA SE", "FCA SK", "FCA UK", "FCA ZA"
]

third_party_tech_list = [
    "4W - Advertising solutions", "AdForm", "Adobe", "Amazon", "AppNexus",
    "Criteo", "Google CM", "Facebook"
]

conversion_types = [
    "Engaged Session", "Landing Page", "Contact Request Start", "Contact Request End",
    "Model Page View", "Configurator Start", "Configurator End"
]

# Streamlit App
st.title("Tag Request Form")

with st.form("tag_request_form"):
    exType = st.selectbox("Type", ["", "exPSA", "exFCA"])
    if exType == "exPSA":
        brands = exPSA_brands
        agencies = exPSA_agencies
    elif exType == "exFCA":
        brands = exFCA_brands
        agencies = exFCA_agencies
    else:
        brands = []
        agencies = []

    brand = st.selectbox("Brand", [""] + brands)
    car_model_choice = st.selectbox("Car Model", ["All Models", "Select a model"])
    if car_model_choice == "Select a model":
        car_model = st.text_input("Type model here")
    else:
        car_model = car_model_choice

    publisher = st.text_input("Publisher")
    url = st.text_input("URL", placeholder="https://example.com")
    pixel_lifetime = st.selectbox("Pixel Lifetime", ["", "Always On", "Campaign only"])
    conversion_type = st.selectbox("Conversion Type", [""] + conversion_types)
    tag_code = st.text_area("Tag Code", height=100)
    third_party_tech = st.selectbox("Third-Party Tech Name", [""] + third_party_tech_list)
    agency_name = st.selectbox("Agency Name", [""] + agencies)
    date = st.date_input("Date", value=datetime.date.today())
    advertiser_name = st.text_input("Advertiser Name")
    instruction = st.text_area("Instruction", height=100)

    submitted = st.form_submit_button("Submit")

if submitted:
    form_data = {
        "Type": exType,
        "Brand": brand,
        "Car Model": car_model,
        "Publisher": publisher,
        "URL": url,
        "Pixel Lifetime": pixel_lifetime,
        "Conversion Type": conversion_type,
        "Tag Code": tag_code,
        "Third-Party Tech Name": third_party_tech,
        "Agency Name": agency_name,
        "Advertiser Name": advertiser_name,
        "Date": date.strftime("%Y-%m-%d"),
        "Instruction": instruction
    }

    # Generate Excel file
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Tag Request")

    # Column widths
    worksheet.set_column("A:A", 30)
    worksheet.set_column("B:B", 60)

    # Formats
    header_format = workbook.add_format({
        'bold': True, 'font_color': 'white', 'bg_color': '#4F81BD',
        'align': 'center', 'valign': 'vcenter', 'border': 1
    })
    label_format = workbook.add_format({'bold': True, 'border': 1, 'valign': 'vcenter'})
    value_format = workbook.add_format({'border': 1, 'valign': 'vcenter'})

    # Title
    worksheet.merge_range('A1:B1', 'Tag Request Form', header_format)

    # Data rows
    row = 1
    for key, value in form_data.items():
        worksheet.write(row, 0, key, label_format)
        worksheet.write(row, 1, value or "", value_format)
        row += 1

    workbook.close()
    output.seek(0)

    filename = f"tag_request_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    st.success("Form submitted! Click below to download the Excel file.")
    st.download_button(label="Download Excel", data=output, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
