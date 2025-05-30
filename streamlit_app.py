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

st.title("Tag Request Form")

with st.form("tag_request_form"):
    exType = st.selectbox("Type *", ["", "exPSA", "exFCA"])
    if exType == "exPSA":
        brands = exPSA_brands
        agencies = exPSA_agencies
    elif exType == "exFCA":
        brands = exFCA_brands
        agencies = exFCA_agencies
    else:
        brands = []
        agencies = []

    brand = st.selectbox("Brand *", [""] + brands)
    car_model_choice = st.selectbox("Car Model *", ["All Models", "Select a model"])
    if car_model_choice == "Select a model":
        car_model = st.text_input("Type model here *")
    else:
        car_model = car_model_choice

    publisher = st.text_input("Publisher *")
    url = st.text_input("URL *", placeholder="https://example.com")
    pixel_lifetime = st.selectbox("Pixel Lifetime *", ["", "Always On", "Campaign only"])
    conversion_type = st.selectbox("Conversion Type *", [""] + conversion_types)
    
    # Replacing tag_code with two checkboxes
    st.markdown("**Tracking Method:**")
    floodlight_selected = st.checkbox("Floodlight")
    pixel_code_selected = st.checkbox("Pixel Code")
    pixel_code_value = ""
    if pixel_code_selected:
        pixel_code_value = st.text_area("Enter Pixel Code *", height=100)

    third_party_tech = st.selectbox("Third-Party Tech Name *", [""] + third_party_tech_list)
    agency_name = st.selectbox("Agency Name *", [""] + agencies)
    
    # Changing date to Expiration Date
    expiration_date = st.date_input("Expiration Date *", value=datetime.date.today())
    
    advertiser_name = st.text_input("Advertiser Name *")
    instruction = st.text_area("Instruction *", height=100)

    submitted = st.form_submit_button("Submit")

if submitted:
    # Validation
    errors = []
    if exType == "":
        errors.append("Please select a Type.")
    if brand == "":
        errors.append("Please select a Brand.")
    if car_model_choice == "Select a model" and not car_model.strip():
        errors.append("Please enter a car model.")
    if publisher.strip() == "":
        errors.append("Publisher is required.")
    if url.strip() == "":
        errors.append("URL is required.")
    if pixel_lifetime == "":
        errors.append("Please select a Pixel Lifetime.")
    if conversion_type == "":
        errors.append("Please select a Conversion Type.")
    if not floodlight_selected and not pixel_code_selected:
        errors.append("Please select at least one tracking method (Floodlight or Pixel Code).")
    if pixel_code_selected and pixel_code_value.strip() == "":
        errors.append("Please enter Pixel Code.")
    if third_party_tech == "":
        errors.append("Please select a Third-Party Tech Name.")
    if agency_name == "":
        errors.append("Please select an Agency Name.")
    if advertiser_name.strip() == "":
        errors.append("Advertiser Name is required.")
    if instruction.strip() == "":
        errors.append("Instruction is required.")

    if errors:
        st.error("Please correct the following errors:\n- " + "\n- ".join(errors))
    else:
        form_data = {
            "Type": exType,
            "Brand": brand,
            "Car Model": car_model,
            "Publisher": publisher,
            "URL": url,
            "Pixel Lifetime": pixel_lifetime,
            "Conversion Type": conversion_type,
            "Tracking Method": "Floodlight" if floodlight_selected else "Pixel Code",
            "Pixel Code": pixel_code_value,
            "Third-Party Tech Name": third_party_tech,
            "Agency Name": agency_name,
            "Expiration Date": expiration_date.strftime("%Y-%m-%d"),
            "Advertiser Name": advertiser_name,
            "Instruction": instruction
        }

        # Generate Excel file
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Tag Request")

        worksheet.set_column("A:A", 30)
        worksheet.set_column("B:B", 60)

        header_format = workbook.add_format({
            'bold': True, 'font_color': 'white', 'bg_color': '#4F81BD',
            'align': 'center', 'valign': 'vcenter', 'border': 1
        })
        label_format = workbook.add_format({'bold': True, 'border': 1, 'valign': 'vcenter'})
        value_format = workbook.add_format({'border': 1, 'valign': 'vcenter'})

        worksheet.merge_range('A1:B1', 'Tag Request Form', header_format)

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
