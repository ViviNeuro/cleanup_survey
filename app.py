
# import streamlit as st
# from datetime import datetime

# # -------------------
# # Page config
# # -------------------
# st.set_page_config(
#     page_title="Trash Management Survey",
#     page_icon="🗑️",
#     layout="centered",
# )

# # -------------------
# # Global CSS: reduce spacing between markdown labels and widgets
# # -------------------
# st.markdown(
#     """
#     <style>
#       /* Reduce bottom margin after markdown blocks (labels) */
#       div[data-testid="stMarkdown"] { margin-bottom: 0.2rem; }

#       /* Reduce top margin before widgets (helps "label -> widget" closeness) */
#       div[data-testid="stVerticalBlock"] > div:has(> div[data-testid^="stWidget"]) {
#         margin-top: -0.2rem;
#       }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.title("Trash Management Survey")

# # -------------------
# # Helpers
# # -------------------
# def float_input(label: str, key: str, step: float = 0.1):
#     """Decimal number input (e.g., 8.5, 0.6)."""
#     return st.number_input(
#         label,
#         min_value=0.0,
#         step=step,
#         format="%.1f",
#         key=key,
#     )

# def build_multiselect_with_other(options: list[str], other_label: str, key_prefix: str):
#     """
#     Returns:
#       selected: list[str] (includes other_label if chosen)
#       other_value: str (free text, stripped)
#     """
#     selected = st.multiselect(
#         label="",  # label handled by markdown above
#         options=options + [other_label],
#         key=f"{key_prefix}_selected",
#     )

#     other_value = ""
#     if other_label in selected:
#         other_value = st.text_input(
#             "Other (please specify):",
#             key=f"{key_prefix}_other_text",
#         ).strip()

#     return selected, other_value

# def normalize_selected(selected: list[str], other_label: str, other_value: str):
#     """
#     Replace other_label with other_value (if provided), otherwise drop it.
#     Returns a clean list of item names.
#     """
#     final_items = []
#     for item in selected:
#         if item == other_label:
#             if other_value:
#                 final_items.append(other_value)
#             else:
#                 st.warning(f"You selected '{other_label}' but didn’t specify a name.")
#         else:
#             final_items.append(item)
#     return final_items

# def collect_value_per_item(items: list[str], what_label: str, key_prefix: str):
#     """
#     For each item in items, ask for a decimal input.
#     Returns dict: {item: value}
#     """
#     values = {}
#     for item in items:
#         values[item] = float_input(
#             f"{what_label} for '{item}':",
#             key=f"{key_prefix}_{what_label.lower().replace(' ', '_')}_{item}",
#         )
#     return values

# # -------------------
# # 1) Homestay
# # -------------------
# st.subheader("1) Homestay")

# homestays = ["Yenbuba", "Bongkso", "Mongkor", "Paparissa", "Kri"]
# OTHER_HOME = "Other (Free text)"

# st.markdown("#### Select your homestay(s)")
# selected_homestays_raw, other_homestay = build_multiselect_with_other(
#     options=homestays,
#     other_label=OTHER_HOME,
#     key_prefix="homestay",
# )

# selected_homestays = normalize_selected(
#     selected=selected_homestays_raw,
#     other_label=OTHER_HOME,
#     other_value=other_homestay,
# )

# # NEW: Bags per homestay (before kg)
# if selected_homestays:
#     st.markdown("#### How many bags per homestay?")
#     homestay_bags = collect_value_per_item(
#         items=selected_homestays,
#         what_label="Bags",
#         key_prefix="homestay",
#     )
# else:
#     homestay_bags = {}

# # Kg per homestay
# if selected_homestays:
#     st.markdown("#### How many kg per homestay?")
#     homestay_kg = collect_value_per_item(
#         items=selected_homestays,
#         what_label="Kg",
#         key_prefix="homestay",
#     )
# else:
#     homestay_kg = {}

# st.divider()

# # -------------------
# # 2) Trash types
# # -------------------
# st.subheader("2) Trash types")

# trash_types = [
#     "sachets",
#     "ropes",
#     "styrofoam",
#     "pop mie",
#     "soft plastics",
#     "medium plastics nr",
#     "medium plastics r",
#     "hard plastics",
#     "clothing",
#     "metal and electronics",
#     "aqua cups",
#     "carton and paper",
#     "plastic bottles",
#     "sandals",
#     "rice bags",
# ]

# st.markdown("#### Select your trash type(s)")
# selected_trash = st.multiselect(
#     label="",
#     options=trash_types,
#     key="trash_selected",
# )

# if selected_trash:
#     st.markdown("#### How many kg per trash type?")
#     trash_kg = collect_value_per_item(
#         items=selected_trash,
#         what_label="Kg",
#         key_prefix="trash",
#     )
# else:
#     trash_kg = {}

# st.divider()

# # -------------------
# # 3) End-uses
# # -------------------
# st.subheader("3) End-use(s)")

# end_uses = ["recycled", "disposed", "reused"]

# st.markdown("#### Select end-use(s)")
# selected_end_uses = st.multiselect(
#     label="",
#     options=end_uses,
#     key="end_uses_selected",
# )

# st.divider()

# # -------------------
# # 4) Cleanup locations
# # -------------------
# st.subheader("4) Cleanup location(s)")

# locations = ["Yenbeser", "Mioskun", "Merpati", "Keruwo", "Kri", "Yenbuba", "Koi"]
# OTHER_LOC = "Other (Free text)"

# st.markdown("#### Select cleanup location(s)")
# selected_locations_raw, other_location = build_multiselect_with_other(
#     options=locations,
#     other_label=OTHER_LOC,
#     key_prefix="location",
# )

# final_locations = normalize_selected(
#     selected=selected_locations_raw,
#     other_label=OTHER_LOC,
#     other_value=other_location,
# )

# st.divider()

# # -------------------
# # Totals
# # -------------------
# st.subheader("Totals")

# total_kg_homestay = round(sum(homestay_kg.values()), 1) if homestay_kg else 0.0
# total_kg_trash = round(sum(trash_kg.values()), 1) if trash_kg else 0.0

# st.markdown(f"#### Total kg (by homestay): **{total_kg_homestay:.1f}**")
# st.markdown(f"#### Total kg (by trash type): **{total_kg_trash:.1f}**")

# if homestay_kg and trash_kg and abs(total_kg_homestay - total_kg_trash) > 0.2:
#     st.info(
#         "Note: totals by homestay and by trash type don’t match exactly. "
#         "That can happen—just double-check if it seems off."
#     )

# st.divider()

# # -------------------
# # Submit
# # -------------------
# if st.button("Submit survey ✅"):
#     payload = {
#         "submitted_at": datetime.utcnow().isoformat(),
#         "homestays": selected_homestays,
#         "homestay_bags": homestay_bags,            # dict
#         "homestay_kg": homestay_kg,                # dict
#         "trash_types": selected_trash,
#         "trash_kg": trash_kg,                      # dict
#         "end_uses": selected_end_uses,             # list
#         "cleanup_locations": final_locations,       # list
#         "total_kg_homestay": total_kg_homestay,
#         "total_kg_trash": total_kg_trash,
#     }

#     st.success("Survey submitted!")
#     st.write("### Summary (what would be saved)")
#     st.json(payload)




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
    md_label(label_md)
    return st.number_input(
        label="",
        min_value=0.0,
        step=0.1,
        format="%.1f",
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
        homestay_bags[h] = number_input_decimal(
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
        location_bags[loc] = number_input_decimal(
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
total_bags_homestay = round(sum(homestay_bags.values()), 1)
total_bags_location = round(sum(location_bags.values()), 1)
total_kg_location = round(sum(location_kg.values()), 1)

st.write(f"**Total bags (by homestay):** {total_bags_homestay:.1f}")
st.write(f"**Total kg (by homestay):** {total_kg_homestay:.1f}")
st.write(f"**Total kg (by trash type):** {total_kg_trash:.1f}")
st.write(f"**Total bags (by cleanup location):** {total_bags_location:.1f}")
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