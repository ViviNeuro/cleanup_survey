import streamlit as st
from datetime import datetime

# -------------------
# Page + styling
# -------------------
st.set_page_config(
    page_title="Trash Management Survey",
    page_icon="🗑️",
    layout="centered",
)

st.markdown(
    """
    <style>
      h4 { margin-bottom: 0.25rem !important; margin-top: 0.75rem !important; }
      h3 { margin-bottom: 0.35rem !important; margin-top: 1.0rem !important; }
      div[data-testid="stWidget"] { margin-top: -0.25rem; }
      hr { margin: 0.8rem 0; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Trash Management Survey")

# -------------------
# Helpers
# -------------------
def md_label(text: str):
    st.markdown(f"#### {text}")

def multiselect_with_other(label_md: str, options: list[str], other_label: str, key_prefix: str):
    md_label(label_md)
    selected = st.multiselect(
        label="",
        options=options + [other_label],
        key=f"{key_prefix}_selected",
        label_visibility="collapsed",
    )

    other_value = ""
    if other_label in selected:
        md_label("Please specify:")
        other_value = st.text_input(
            label="",
            key=f"{key_prefix}_other_text",
            label_visibility="collapsed",
        ).strip()

    return selected, other_value

def number_input_decimal(label_md: str, key: str):
    """For kg (floats like 8.5, 0.6)"""
    md_label(label_md)
    return st.number_input(
        label="",
        min_value=0.0,
        step=0.1,
        format="%.1f",
        key=key,
        label_visibility="collapsed",
    )

def number_input_integer(label_md: str, key: str):
    """For bags (integers only)"""
    md_label(label_md)
    return st.number_input(
        label="",
        min_value=0,
        step=1,
        format="%d",
        key=key,
        label_visibility="collapsed",
    )

def selectbox_md(label_md: str, options: list[str], key: str):
    md_label(label_md)
    return st.selectbox(
        label="",
        options=options,
        key=key,
        label_visibility="collapsed",
    )

# -------------------
# 1) Homestay
# -------------------
st.subheader("1) Homestay")

homestays = ["Yenbuba", "Bongkso", "Mongkor", "Paparissa", "Kri"]
OTHER_HOME = "Other (Free text)"

selected_homestays_raw, other_homestay = multiselect_with_other(
    "Select your homestay(s):",
    homestays,
    OTHER_HOME,
    "homestay",
)

selected_homestays = []
for h in selected_homestays_raw:
    if h == OTHER_HOME:
        if other_homestay:
            selected_homestays.append(other_homestay)
        else:
            st.warning("You selected 'Other' but didn’t specify a homestay.")
    else:
        selected_homestays.append(h)

homestay_bags = {}
homestay_kg = {}

if selected_homestays:
    st.markdown("##### Homestay details")

    for h in selected_homestays:
        homestay_bags[h] = number_input_integer(
            f"How many bags for '{h}'?",
            key=f"bags_{h}",
        )

    st.divider()

    for h in selected_homestays:
        homestay_kg[h] = number_input_decimal(
            f"How many kg of trash from '{h}'?",
            key=f"kg_{h}",
        )

st.divider()

# -------------------
# 2) Trash types
# -------------------
st.subheader("2) Trash types")

trash_types = [
    "sachets",
    "ropes",
    "styrofoam",
    "pop mie",
    "soft plastics",
    "medium plastics nr",
    "medium plastics r",
    "hard plastics",
    "clothing",
    "metal and electronics",
    "aqua cups",
    "carton and paper",
    "plastic bottles",
    "sandals",
    "rice bags",
]

md_label("Select trash type(s):")
selected_trash = st.multiselect(
    label="",
    options=trash_types,
    key="trash_selected",
    label_visibility="collapsed",
)

end_use_options = ["recycled", "disposed", "reused"]
trash_details = {}

if selected_trash:
    st.markdown("##### Trash details")

    for t in selected_trash:
        kg_val = number_input_decimal(
            f"How many kg of '{t}'?",
            key=f"trash_kg_{t}",
        )
        end_use_val = selectbox_md(
            f"End-use for '{t}':",
            end_use_options,
            key=f"end_use_{t}",
        )
        trash_details[t] = {"kg": kg_val, "end_use": end_use_val}

st.divider()

# -------------------
# 3) Cleanup locations
# -------------------
st.subheader("3) Cleanup location(s)")

locations = ["Yenbeser", "Mioskun", "Merpati", "Keruwo", "Kri", "Yenbuba", "Koi"]
OTHER_LOC = "Other (Free text)"

selected_locations_raw, other_location = multiselect_with_other(
    "Select cleanup location(s):",
    locations,
    OTHER_LOC,
    "location",
)

selected_locations = []
for loc in selected_locations_raw:
    if loc == OTHER_LOC:
        if other_location:
            selected_locations.append(other_location)
        else:
            st.warning("You selected 'Other' but didn’t specify a location.")
    else:
        selected_locations.append(loc)

location_bags = {}
location_kg = {}

if selected_locations:
    st.markdown("#### Cleanup location details")

    for loc in selected_locations:
        location_bags[loc] = number_input_integer(
            f"How many bags from '{loc}'?",
            key=f"location_bags_{loc}",
        )

    st.divider()

    for loc in selected_locations:
        location_kg[loc] = number_input_decimal(
            f"How many kg from '{loc}'?",
            key=f"location_kg_{loc}",
        )

st.divider()

# -------------------
# Totals
# -------------------
st.subheader("Totals")

total_kg_homestay = round(sum(homestay_kg.values()), 1)
total_kg_trash = round(sum(v["kg"] for v in trash_details.values()), 1)
total_bags_homestay = sum(homestay_bags.values())
total_bags_location = sum(location_bags.values())
total_kg_location = round(sum(location_kg.values()), 1)

st.write(f"**Total bags (by homestay):** {total_bags_homestay}")
st.write(f"**Total kg (by homestay):** {total_kg_homestay:.1f}")
st.write(f"**Total kg (by trash type):** {total_kg_trash:.1f}")
st.write(f"**Total bags (by cleanup location):** {total_bags_location}")
st.write(f"**Total kg (by cleanup location):** {total_kg_location:.1f}")

st.divider()

# -------------------
# Submit
# -------------------
if st.button("Submit survey"):
    payload = {
        "submitted_at": datetime.utcnow().isoformat(),
        "homestays": selected_homestays,
        "homestay_bags": homestay_bags,
        "homestay_kg": homestay_kg,
        "trash_details": trash_details,
        "cleanup_locations": selected_locations,
        "location_bags": location_bags,
        "location_kg": location_kg,
        "total_bags_homestay": total_bags_homestay,
        "total_kg_homestay": total_kg_homestay,
        "total_kg_trash": total_kg_trash,
        "total_bags_location": total_bags_location,
        "total_kg_location": total_kg_location,
    }

    st.success("Survey submitted!")
    st.write("### Summary")
    st.json(payload)