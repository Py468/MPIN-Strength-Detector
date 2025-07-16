import streamlit as st
from datetime import datetime
from code import MPINChecker

checker = MPINChecker()

st.set_page_config(page_title="MPIN Strength Checker", layout="centered")
st.title("🔐 MPIN Strength Checker")
st.write("Check if your mobile banking MPIN is weak or strong.")

mpin = st.text_input("Enter your MPIN (4 or 6 digits)", max_chars=6)
dob_self = st.date_input("Your Date of Birth", value=datetime(2000, 1, 1))
dob_spouse = st.date_input("Spouse's Date of Birth (optional)", value=datetime(1995, 1, 1), min_value=datetime(1900, 1, 1), max_value=datetime.today())
anniversary = st.date_input("Wedding Anniversary (optional)", value=datetime(2020, 1, 1), min_value=datetime(1900, 1, 1), max_value=datetime.today())


if st.button("Check Strength"):
    if not mpin.isdigit() or len(mpin) not in [4, 6]:
        st.error("MPIN must be a 4 or 6 digit number")
    else:

        format_date = lambda d: d.strftime("%d-%m-%Y") if d else ""
        demographics = {
            "dob_self": format_date(dob_self),
            "dob_spouse": format_date(dob_spouse),
            "anniversary": format_date(anniversary),
        }

        result = checker.check_mpin_strength(mpin, demographics)

        if result['Strength'] == "WEAK":
            st.error("🚫 MPIN is WEAK")
            st.write("### Reasons:")
            for reason in result['Reasons']:
                st.write(f"- {reason}")
        else:
            st.success("✅ MPIN is STRONG")
