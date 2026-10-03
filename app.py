import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from rembg import remove
import io

st.set_page_config(page_title="Poster Generator", layout="centered")
st.title("🎓 Student Poster Generator")

# Form Controls
student_name = st.text_input("Student Name", "NAKSHATHRA RATHEESH")
student_class = st.text_input("Class / Division", "(2B)")
uploaded_file = st.file_uploader("Upload Student Photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    if st.button("Generate Poster"):
        with st.spinner("Processing background removal & rendering poster..."):
            # Load template
            template = Image.open("template.png").convert("RGBA")

            # Cutout student background
            input_image = Image.open(uploaded_file)
            cutout = remove(input_image)

            # Resize cutout and composite onto template
            cutout = cutout.resize((450, 600))
            template.paste(cutout, (80, 180), cutout)

            # Draw student name and class
            draw = ImageDraw.Draw(template)
            try:
                font_name = ImageFont.truetype("arialbd.ttf", 36)
                font_class = ImageFont.truetype("arialbd.ttf", 30)
            except:
                font_name = ImageFont.load_default()
                font_class = ImageFont.load_default()

            draw.text((520, 510), student_name.upper(), fill="#004D25", font=font_name)
            draw.text((580, 560), student_class, fill="#004D25", font=font_class)

            # Show output preview
            st.image(template, caption="Generated Poster", use_column_width=True)

            # Download Action
            buf = io.BytesIO()
            template.convert("RGB").save(buf, format="JPEG")
            st.download_button(
                label="📥 Download Poster",
                data=buf.getvalue(),
                file_name=f"{student_name.replace(' ', '_')}_poster.jpg",
                mime="image/jpeg"
            )