import streamlit as st
import html
from difflib import ndiff
from PIL import Image

def highlight_differences(text1, text2):
    """实时高亮文本差异"""
    diff = list(ndiff(text1, text2))
    highlighted_text1 = ""  # 修改前文本
    highlighted_text2 = ""  # 修改后文本

    for d in diff:
        if d.startswith('- '):
            highlighted_text1 += f'<span style="background-color:#ffcccb">{html.escape(d[2:])}</span>'
        elif d.startswith('+ '):
            highlighted_text2 += f'<span style="background-color:#90EE90">{html.escape(d[2:])}</span>'
        else:
            highlighted_text1 += html.escape(d[2:])
            highlighted_text2 += html.escape(d[2:])

    return highlighted_text1.strip(), highlighted_text2.strip()  # 去掉空白行

def main():
    st.set_page_config(layout="wide")

    image = Image.open("logo.png")
    st.image(image, width=80)

    st.markdown('<h2 style="text-align: center; color: #4BA6E0;font-size: 48px;">文本对比工具</h2>', unsafe_allow_html=True)

    # 初始化存储数据
    if "texts" not in st.session_state:
        st.session_state.texts = [{"修改前": "", "修改后": ""} for _ in range(2)]

    # 渲染文本框界面
    for i in range(len(st.session_state.texts)):
        st.write(f"### 第 {i+1} 行")

        col1, col2 = st.columns([1, 1])
        with col1:
            st.session_state.texts[i]["修改前"] = st.text_area(
                "修改前",
                st.session_state.texts[i]["修改前"],
                key=f"old_{i}",
                height=100,  # 设置文本框高度为100，减少空白区域
                max_chars=2000
            )

        with col2:
            st.session_state.texts[i]["修改后"] = st.text_area(
                "修改后",
                st.session_state.texts[i]["修改后"],
                key=f"new_{i}",
                height=100,  # 设置文本框高度为100，减少空白区域
                max_chars=2000
            )

        # 计算高亮对比
        highlighted_text1, highlighted_text2 = highlight_differences(
            st.session_state.texts[i]["修改前"],
            st.session_state.texts[i]["修改后"]
        )

        # 在文本框下方显示高亮对比
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(
                f"""
                <div style="white-space: pre-wrap; border: 1px solid #bbb; padding: 3px; border-radius: 3px; background-color: #f3f3f3; font-size: 14px;">
                    {highlighted_text1}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div style="white-space: pre-wrap; border: 1px solid #bbb; padding: 3px; border-radius: 3px; background-color: #f3f3f3; font-size: 14px;">
                    {highlighted_text2}
                </div>
                """,
                unsafe_allow_html=True
            )

    # 添加行按钮
    col_space, col_buttons = st.columns([9, 1])
    with col_buttons:
        if st.button("➕ 添加行"):
            st.session_state.texts.append({"修改前": "", "修改后": ""})
            st.rerun()  # 触发页面更新

if __name__ == "__main__":
    main()
