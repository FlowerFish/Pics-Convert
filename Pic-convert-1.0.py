import streamlit as st
from PIL import Image
import io
import zipfile

SUPPORTED_INPUT_FORMATS = ["jpeg", "jpg", "png", "gif", "webp"]
OUTPUT_FORMATS = ["PNG", "JPEG", "GIF", "WEBP"]

def convert_image(uploaded_file, output_format):
    """將上傳的圖片檔案轉換為指定的格式。"""
    try:
        img = Image.open(uploaded_file)
        input_format = img.format.lower()
        if input_format not in SUPPORTED_INPUT_FORMATS:
            st.error(f"不支援的輸入檔案格式：{img.format}")
            return None

        output_buffer = io.BytesIO()
        img.save(output_buffer, format=output_format.upper())
        return output_buffer
    except Exception as e:
        st.error(f"轉換過程中發生錯誤：{e}")
        return None

def create_zip_from_buffers(buffers, output_format):
    """將多個圖片緩衝區打包成一個 ZIP 檔案。"""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for i, buffer in enumerate(buffers):
            file_name = f"converted_{i + 1}.{output_format.lower()}"
            zipf.writestr(file_name, buffer.getvalue())
    zip_buffer.seek(0)
    return zip_buffer

def main():
    st.set_page_config(page_title="圖片格式轉換器", page_icon="📸", layout="centered")

    st.markdown(
        """
        <style>
        .main-title {
            font-size: 4em;
            color: #4CAF50;
            text-align: center;
            margin-bottom: 0;
        }
        .subtitle {
            font-size: 1.5em;
            color: #555;
            text-align: center;
        }
        .version {
            font-size: 1em;
            color: #777;
            text-align: center;
            margin-top: 0;
        }
        .upload-box {
            border: 2px dashed #4CAF50;
            padding: 20px;
            border-radius: 10px;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 12px;
        }
        .button:hover {
            background-color: #45a049;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="main-title">圖片格式轉換器</div>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">(支援 JPEG, PNG, GIF, Webp)</p>', unsafe_allow_html=True)
    st.markdown('<p class="version">版本 Ver: 1.0 | 2025 | 作者：Aries Yeh</p>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "上傳你的圖片檔案", type=SUPPORTED_INPUT_FORMATS, accept_multiple_files=True
    )

    if uploaded_files:
        st.markdown('<p class="subtitle">上傳的圖片:</p>', unsafe_allow_html=True)
        for uploaded_file in uploaded_files:
            st.image(uploaded_file, width=200)

        output_format = st.selectbox(
            "選擇轉換後的格式:", OUTPUT_FORMATS
        )

        if st.button("轉換", key="convert_button"):
            buffers = []
            for uploaded_file in uploaded_files:
                output_buffer = convert_image(uploaded_file, output_format)
                if output_buffer:
                    buffers.append(output_buffer)

            if buffers:
                zip_buffer = create_zip_from_buffers(buffers, output_format)
                st.markdown('<p class="subtitle">轉換後的 ZIP 檔案:</p>', unsafe_allow_html=True)
                st.download_button(
                    label=f"下載所有轉換後的 {output_format} 檔案",
                    data=zip_buffer,
                    file_name=f"converted_images.zip",
                    mime="application/zip"
                )

if __name__ == "__main__":
    main()
