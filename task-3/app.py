import streamlit as st
from password_strength import PasswordStats
import random
import string

def generate_password(length=12, use_digits=True, use_specials=True):
    chars = string.ascii_letters
    if use_digits:
        chars += string.digits
    if use_specials:
        chars += string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def analyze_password(password):
    stats = PasswordStats(password)
    strength = stats.strength()
    feedback = []
    
    if len(password) < 8:
        feedback.append("Increase password length (at least 8 characters recommended)")
    if not any(char.isdigit() for char in password):
        feedback.append("Add numbers to strengthen your password")
    if not any(char in string.punctuation for char in password):
        feedback.append("Include special characters for better security")
    if not any(char.isupper() for char in password):
        feedback.append("Use uppercase letters to enhance security")
    
    return strength, feedback

# Streamlit UI
st.set_page_config(page_title="Password Strength Checker", layout="wide")

st.markdown("<h2 style='text-align: center;'>🔒 Password Strength Meter & Generator</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Check Your Password Strength")
    password = st.text_input("Enter Password:", type="password")
    if password:
        strength, feedback = analyze_password(password)
        
        strength_label = "Weak" if strength < 0.3 else "Moderate" if strength < 0.7 else "Strong"
        strength_color = "#e63946" if strength < 0.3 else "#f4a261" if strength < 0.7 else "#2a9d8f"
        
        st.markdown(f"""<div style='background:{strength_color}; padding:8px; border-radius:5px; text-align:center; font-size:16px; color:white;'>
                    Strength: {strength_label}
                    </div>""", unsafe_allow_html=True)
        
        if feedback:
            st.markdown("**Suggestions:**")
            for tip in feedback:
                st.markdown(f"- {tip}")

with col2:
    st.subheader("⚡ Generate a Secure Password")
    length = st.slider("Password Length", min_value=8, max_value=32, value=12)
    use_digits = st.checkbox("Include Numbers", value=True)
    use_specials = st.checkbox("Include Special Characters", value=True)
    
    if st.button("Generate Password"):
        generated_password = generate_password(length, use_digits, use_specials)
        st.text_input("Generated Password:", value=generated_password, disabled=True)
        
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("<h5 style='text-align: center;'>✅ Compact, Fast, and Easy-to-Use Password Manager</h5>", unsafe_allow_html=True)
