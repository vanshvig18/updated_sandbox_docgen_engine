import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Template Mapping", layout="wide")

# Login-state-safe groq_outputs
if 'groq_outputs' not in st.session_state:
    st.session_state['groq_outputs'] = {}

# Groq Config
groq_api_key = "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"
groq_url = "https://api.groq.com/openai/v1/chat/completions"

def query_groq(prompt):
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }
    res = requests.post(groq_url, headers=headers, json=body)
    if res.status_code == 200:
        return res.json()['choices'][0]['message']['content']
    else:
        return f"Error: {res.status_code}"

# Sidebar + Upload check
st.sidebar.title("📚 Navigation")
st.sidebar.markdown("### ➤ main")
st.sidebar.markdown("### ➤ Auth")
st.sidebar.markdown("### ➤ Document Uploader")
st.sidebar.markdown("### **Template Mapping**", help="You're here")

st.markdown("<h2 style='color:#00FFAA;'>🧾 Template Mapping with Subsections</h2>", unsafe_allow_html=True)

if 'uploaded_data' not in st.session_state:
    st.warning("⚠️ Please upload files first on the Document Uploader page.")
    st.stop()

uploaded_data = st.session_state['uploaded_data']
file_options = list(uploaded_data.keys())

# Section → Subsection Map
section_subsections = {
    "Overview": ["Summary", "Context"],
    "Motivation": ["Business Need", "Scientific Relevance", "Stakeholder Goals"],
    "Problem": ["Challenges", "Constraints"],
    "Data": ["Sources", "Quality", "Preprocessing"],
    "Success": ["KPIs", "Expected Outcomes"]
}

# MAIN UI LOOP
for section, subsections in section_subsections.items():
    st.markdown(f"## 🗂️ {section}")
    
    for subsection in subsections:
        st.markdown(f"#### ✏️ {subsection}")
        
        selected_files = st.multiselect(f"Select file(s) for '{section} → {subsection}'", options=file_options, key=f"files_{section}_{subsection}")
        prompt = st.text_area(f"Prompt for '{subsection}'", key=f"prompt_{section}_{subsection}")
        
        if st.button(f"Generate with Groq for {section} → {subsection}", key=f"btn_{section}_{subsection}"):
            combined_chunks = []
            for f in selected_files:
                if f in uploaded_data:
                    data = uploaded_data[f]
                    header = f"\n### Content from file: {f}\n"
                    if isinstance(data, pd.DataFrame):
                        content = data.to_string(index=False)
                    elif isinstance(data, str):
                        content = data
                    else:
                        try:
                            content = str(data)
                        except:
                            content = "[Unsupported data format]"
                    combined_chunks.append(header + content)

            combined_text = "\n\n".join(combined_chunks)
            full_prompt = f"{prompt}\n\n{combined_text}"
            output = query_groq(full_prompt)
            
            # Save to session state
            if section not in st.session_state['groq_outputs']:
                st.session_state['groq_outputs'][section] = {}
            st.session_state['groq_outputs'][section][subsection] = output
            
            st.success("✅ Response Received")
            st.code(output)

st.markdown("---")
st.info("Once done, export the mapped results:")

# Export Logic
if st.session_state['groq_outputs']:
    final_text = ""
    for section, subs in st.session_state['groq_outputs'].items():
        final_text += f"\n\n## {section}\n"
        for sub, result in subs.items():
            final_text += f"\n### {sub}\n{result}\n"

    buffer = io.StringIO(final_text)
    st.download_button(
        label="📥 Download Final Document (.txt)",
        data=buffer.getvalue(),
        file_name="final_document.txt",
        mime="text/plain"
    )
else:
    st.warning("⚠️ No generated content to export.")
