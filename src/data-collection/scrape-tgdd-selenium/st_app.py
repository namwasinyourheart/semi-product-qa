import streamlit as st
import json
from pathlib import Path
json_data = []
with open("H:/My Drive/projects/scrapy-toy/tgdd-selenium/output/product_data/phone_products_20240403_020636.json", "r", encoding="utf-8") as file:
    for line in file:
        json_data.append(json.loads(line))



example1 = json_data[10]

general_info = example1['color_versions']

# Create tables for general_info
general_info_table = "<table>"
for category, specs in general_info.items():
    if isinstance(specs, dict):
        general_info_table += f"<tr><th colspan='2'>{category}</th></tr>"
        for key, value in specs.items():
            general_info_table += f"<tr><td>{key}</td><td>{value}</td></tr>"
    elif isinstance(specs, list):
        general_info_table += f"<tr><th colspan='2'>{category}</th></tr>"
        for item in specs:
            general_info_table += f"<tr><td colspan='2'>{item}</td></tr>"
    else:
        general_info_table += f"<tr><td>{category}</td><td>{specs}</td></tr>"
general_info_table += "</table>"
st.write(general_info_table, unsafe_allow_html=True)


# Create tables for tech_specs
tech_specs_table = "<table>"
for category, specs in example1['tech_specs'].items():
    tech_specs_table += f"<tr><th colspan='2'>{category}</th></tr>"
    for key, value in specs.items():
        tech_specs_table += f"<tr><td>{key}</td><td>{value}</td></tr>"
tech_specs_table += "</table>"
st.write(tech_specs_table, unsafe_allow_html=True)

# Set page configuration
st.set_page_config(layout="wide")

# Streamlit app
st.title("Product Information")
st.write(general_info)

st.subheader("URL")
st.write(example1['url'])


col1, col2 = st.columns([2,1])

with col1: 
    st.subheader("Technical Specifications")
    tech_specs = example1['tech_specs']

with col2: 
    # st.header("Product Information")
    # tech_info = example1['info']
    # st.write(tech_info)

     # Question and Answer Section
    st.subheader("Question and Answer")
    question = st.text_input("Ask your question here:")
    if question:
        # Simple hardcoded question answering for demonstration
        answer = "This is a sample answer to your question."
        st.write("Answer:", answer)

with col1: 
    # Split the layout into two columns
    col1, col2, col3 = st.columns([1,1,1])

    first_half_specs = {k: v for i, (k, v) in enumerate(tech_specs.items()) if i < 3}
    second_half_specs = {k: v for i, (k, v) in enumerate(tech_specs.items()) if i >= 3 and i< 5}
    third_half_specs = {k: v for i, (k, v) in enumerate(tech_specs.items()) if i >= 5 and i< len(tech_specs)}


    with col1:
        tech_specs_table = "<table>"
        for category, specs in first_half_specs.items():
            # print(category, specs)
            tech_specs_table += f"<tr><th colspan='2'>{category}</th></tr>"
            for key, value in specs.items():
                tech_specs_table += f"<tr><td>{key}</td><td>{value}</td></tr>"
        tech_specs_table += "</table>"
        st.write(tech_specs_table, unsafe_allow_html=True)

    with col2:
        tech_specs_table = "<table>"
        for category, specs in second_half_specs.items():
            # print(category, specs)
            tech_specs_table += f"<tr><th colspan='2'>{category}</th></tr>"
            for key, value in specs.items():
                tech_specs_table += f"<tr><td>{key}</td><td>{value}</td></tr>"
        tech_specs_table += "</table>"
        st.write(tech_specs_table, unsafe_allow_html=True)

    with col3:
        tech_specs_table = "<table>"
        for category, specs in third_half_specs.items():
            # print(category, specs)
            tech_specs_table += f"<tr><th colspan='2'>{category}</th></tr>"
            for key, value in specs.items():
                tech_specs_table += f"<tr><td>{key}</td><td>{value}</td></tr>"
        tech_specs_table += "</table>"
        st.write(tech_specs_table, unsafe_allow_html=True)

