import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Make sure we can import audit_service
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from audit_service.core import run_audit_input, run_audit_output
from audit_service.services.gemini_adapter import GeminiAdapter

# Initialize Gemini adapter
gemini = GeminiAdapter()

# Page settings
st.set_page_config(page_title="AI Auditor", layout="wide")

st.markdown("""
    <style>
        .title-text { font-size: 40px !important; font-weight: bold; }
        .subtitle-text { font-size: 20px; color: gray; }
        .card {
            padding: 10px 20px;
            border-radius: 10px;
            background-color: #f9f9f9;
            margin-bottom: 10px;
        }
        .fail { background-color: #ffe6e6; }
        .pass { background-color: #e6ffe6; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-text">🛡️ AI Auditor Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Audit and sanitize prompts or AI outputs for safety, PII, and policy violations.</div>', unsafe_allow_html=True)

tabs = st.tabs(["👤 User Prompt Audit", "🤖 AI Output Audit"])


with tabs[0]:
    st.header("🧾 Audit User Prompt")

    user_prompt = st.text_area("✍️ Enter user prompt:", height=150, key="user_input")

    if st.button("🚦 Run Audit", key="audit_input"):
        if not user_prompt.strip():
            st.warning("⚠️ Please enter a user prompt.")
        else:
            with st.spinner("🔍 Analyzing user input..."):
                results = run_audit_input(user_prompt)

            outcome = results.get("outcome", "UNKNOWN")

            if outcome in ["FAIL", "FLAG"]:
                reason = results["messages"][0] if results.get("messages") else "⚠️ Policy violation detected"
                st.error(f"❌ Blocked — Reason: {reason}")

                if results.get("findings", {}).get("pii", {}).get("found"):
                    st.subheader("🔎 Detected PII")
                    for item in results["findings"]["pii"]["types"]:
                        st.markdown(f"""
                            <div class="card fail">
                                <strong>Type:</strong> {item['type']} |
                                <strong>Severity:</strong> {item['severity']} |
                                <strong>Match:</strong> <code>{item['match'].strip()}</code>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.success("✅ Passed — No issues detected in input.")

            with st.expander("📋 Full Audit Report", expanded=False):
                st.json(results)


with tabs[1]:
    st.header("🤖 Audit AI Output")

    ai_output = st.text_area("✍️ Paste AI response to audit:", height=150, key="ai_output")

    if st.button("🚦 Run Audit", key="audit_output"):
        if not ai_output.strip():
            st.warning("⚠️ Please enter AI output.")
        else:
            with st.spinner("🔍 Auditing AI output..."):
                results = run_audit_output(ai_output)

            with st.expander("📋 Full Audit Report", expanded=False):
                st.json(results)

            flagged_issues = [flag for flag, val in results.get("flags", {}).items() if val > 0]

            if flagged_issues:
                st.warning(f"⚠️ Issues detected: {', '.join(flagged_issues)}")

                with st.spinner("🛠 Rewriting output with Gemini..."):
                    rewritten = gemini.sanitize(ai_output, results["flags"], results)

                st.subheader("📝 Gemini Rewrite")
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Original Output**")
                    st.code(ai_output, language="markdown")

                with col2:
                    st.markdown("**Sanitized Output**")
                    st.code(rewritten, language="markdown")
            else:
                st.success("✅ Output Passed Audit — No rewrite required.")
