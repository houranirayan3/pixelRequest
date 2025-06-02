import streamlit as st
from io import BytesIO
import datetime
import xlsxwriter
from supabase import create_client, Client

# Supabase setup
SUPABASE_URL = "https://dayfbwjqjjrhbaimnava.supabase.co"  # Replace with your project URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRheWZid2pxampyaGJhaW1uYXZhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg2MDgwMzIsImV4cCI6MjA2NDE4NDAzMn0.uTA76vPf2650CElaq3EyTNrLdQwBNYTjM2H712XnFUs"                     # Replace with your anon key
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load options dynamically
@st.cache_data
def load_options():
    brands = supabase.table("brands").select("*").execute().data or []
    agencies = supabase.table("agencies").select("*").execute().data or []
    techs = supabase.table("third_party_tech").select("*").execute().data or []
    conversions = supabase.table("conversion_types").select("*").execute().data or []
    return brands, agencies, techs, conversions

brands_data, agencies_data, tech_data, conv_data = load_options()

# Streamlit App
st.title("Tag Request Form")
with st.form("tag_request_form"):
    exType = st.selectbox("Type", ["", "exPSA", "exFCA"])
    
    # Filter brands and agencies by type
    filtered_brands = [b["name"] for b in brands_data if b.get("type") == exType] if exType else []
    filtered_agencies = [a["name"] for a in agencies_data if a.get("type") == exType] if exType else []
    
    brand = st.selectbox("Brand", [""] + filtered_brands)
    car_model_choice = st.selectbox("Car Model", ["All Models", "Select a model"])
    car_model = st.text_input("Type model here") if car_model_choice == "Select a model" else car_model_choice
    publisher = st.text_input("Publisher")
    url = st.text_input("URL", placeholder="https://example.com")
    pixel_lifetime = st.selectbox("Pixel Lifetime", ["", "Always On", "Campaign only"])
    conversion_type = st.selectbox("Conversion Type", [""] + [c["name"] for c in conv_data])
    tag_code = st.text_area("Tag Code", height=100)
    third_party_tech = st.selectbox("Third-Party Tech Name", [""] + [t["name"] for t in tech_data])
    agency_name = st.selectbox("Agency Name", [""] + filtered_agencies)
    date = st.date_input("Date", value=datetime.date.today())
    advertiser_name = st.text_input("Advertiser Name")
    instruction = st.text_area("Instruction", height=100)
    submitted = st.form_submit_button("Submit")

if submitted:
    form_data = {
        "type": exType,
        "brand": brand,
        "car_model": car_model,
        "publisher": publisher,
        "url": url,
        "pixel_lifetime": pixel_lifetime,
        "conversion_type": conversion_type,
        "tag_code": tag_code,
        "third_party_tech_name": third_party_tech,
        "agency_name": agency_name,
        "advertiser_name": advertiser_name,
        "date": date.isoformat(),
        "instruction": instruction,
        "created_at": datetime.datetime.now().isoformat()
    }
    response = supabase.table("tag_requests").insert(form_data).execute()
    if response.status_code == 201:
        st.success("Form submitted and data saved to Supabase!")
    else:
        st.error(f"Error saving to Supabase: {response.data}")

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Tag Request")
    worksheet.set_column("A:A", 30)
    worksheet.set_column("B:B", 60)
    header_format = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#4F81BD',
                                         'align': 'center', 'valign': 'vcenter', 'border': 1})
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
    st.download_button(label="Download Excel", data=output, file_name=filename,
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
