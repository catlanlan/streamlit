import streamlit as st
import pandas as pd
import html
import fitz  # PyMuPDF for PDF handling
import docx  # python-docx for Word handling
from difflib import ndiff


def highlight_differences(text1, text2):
    diff = list(ndiff(str(text1), str(text2)))
    highlighted_text1, highlighted_text2 = "", ""

    for d in diff:
        if d.startswith('- '):
            highlighted_text1 += f'<span style="background-color:#ffcccb">{html.escape(d[2:])}</span>'
        elif d.startswith('+ '):
            highlighted_text2 += f'<span style="background-color:#90EE90">{html.escape(d[2:])}</span>'
        else:
            highlighted_text1 += html.escape(d[2:])
            highlighted_text2 += html.escape(d[2:])

    return highlighted_text1, highlighted_text2


def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = "\n".join([page.get_text("text") for page in doc])
    return text


def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


def compare_texts(text1, text2):
    return highlight_differences(text1, text2)


def main():
    st.title("📊 文本、表格、文档对比工具")
    st.markdown("支持文本、Excel、CSV、PDF 和 Word 文件对比。")

    tab1, tab2, tab3 = st.tabs(["🔤 文本对比", "📄 表格对比", "📂 文档对比"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            original_text = st.text_area("修改前文本", height=200)
        with col2:
            modified_text = st.text_area("修改后文本", height=200)

        if st.button("Compare Texts 🚀"):
            highlighted_original, highlighted_modified = compare_texts(original_text, modified_text)
            st.session_state.history.append((highlighted_original, highlighted_modified))
            st.success("对比完成！✨")

        if "history" not in st.session_state:
            st.session_state.history = []

        if st.session_state.history:
            st.write("### 📜 历史对比记录")
            for idx, (old, new) in enumerate(reversed(st.session_state.history), 1):
                st.markdown(f"**对比记录 {idx}**")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"<div style='padding:10px; border:1px solid #ddd'>{old}</div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div style='padding:10px; border:1px solid #ddd'>{new}</div>", unsafe_allow_html=True)
                st.markdown("---")

    with tab2:
        st.write("请上传两个文件进行表格对比（支持 CSV 或 Excel）。")
        file1 = st.file_uploader("上传修改前的表格", type=["csv", "xlsx"], key="file1")
        file2 = st.file_uploader("上传修改后的表格", type=["csv", "xlsx"], key="file2")

        if file1 and file2 and st.button("Compare Tables 🚀"):
            try:
                df1 = pd.read_csv(file1) if file1.name.endswith(".csv") else pd.read_excel(file1)
                df2 = pd.read_csv(file2) if file2.name.endswith(".csv") else pd.read_excel(file2)

                if df1.shape != df2.shape:
                    st.error("两张表格的形状不同，无法对比！")
                else:
                    st.write("### 🧐 对比结果")
                    st.dataframe(pd.concat([df1, df2], axis=1))
                    st.success("表格对比完成！✨")
            except Exception as e:
                st.error(f"文件读取失败: {e}")

    with tab3:
        st.write("请上传两个文档（PDF 或 Word）进行对比。")
        doc1 = st.file_uploader("上传修改前的文档", type=["pdf", "docx"], key="doc1")
        doc2 = st.file_uploader("上传修改后的文档", type=["pdf", "docx"], key="doc2")

        if doc1 and doc2 and st.button("Compare Documents 🚀"):
            try:
                text1 = extract_text_from_pdf(doc1) if doc1.name.endswith(".pdf") else extract_text_from_docx(doc1)
                text2 = extract_text_from_pdf(doc2) if doc2.name.endswith(".pdf") else extract_text_from_docx(doc2)

                highlighted_original, highlighted_modified = compare_texts(text1, text2)
                st.write("### 📑 文档对比结果")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"<div style='padding:10px; border:1px solid #ddd'>{highlighted_original}</div>",
                                unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div style='padding:10px; border:1px solid #ddd'>{highlighted_modified}</div>",
                                unsafe_allow_html=True)
                st.success("文档对比完成！✨")
            except Exception as e:
                st.error(f"文档处理失败: {e}")


if __name__ == "__main__":
    main()
