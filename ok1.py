import streamlit as st
from difflib import ndiff
import html

def highlight_differences(text1, text2):
    diff = list(ndiff(text1, text2))
    highlighted_text1 = ""  # 修改前文本
    highlighted_text2 = ""  # 修改后文本

    for d in diff:
        if d.startswith('- '):
            highlighted_text1 += f'<span style="background-color:#ffcccb">{html.escape(d[2:])}</span>'  # 红色高亮删除部分
        elif d.startswith('+ '):
            highlighted_text2 += f'<span style="background-color:#90EE90">{html.escape(d[2:])}</span>'  # 绿色高亮新增部分
        else:
            highlighted_text1 += html.escape(d[2:])
            highlighted_text2 += html.escape(d[2:])

    return highlighted_text1, highlighted_text2


def main():
    st.title("📝 文本对比工具")
    st.write("在左侧输入原文本，在右侧输入修改后的文本，点击 Compare 进行对比。")

    if "history" not in st.session_state:
        st.session_state.history = []

    col1, col2 = st.columns(2)
    with col1:
        original_text = st.text_area("修改前文本", height=200)
    with col2:
        modified_text = st.text_area("修改后文本", height=200)

    if st.button("Compare 🚀"):
        highlighted_original, highlighted_modified = highlight_differences(original_text, modified_text)
        st.session_state.history.append((highlighted_original, highlighted_modified))
        st.success("对比完成！✨")

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


if __name__ == "__main__":
    main()
