import streamlit as st
from yt_dlp import YoutubeDL
import os

st.set_page_config(page_title="ToolVideo01 PRO MAX", layout="centered")

st.title("🎬 ToolVideo01 PRO MAX")
st.caption("Download YouTube Video + Playlist (MP4 / MP3)")

url = st.text_input("🔗 Nhập link YouTube hoặc Playlist:")

mode = st.radio("📌 Chế độ:", ["🎥 Video / Playlist", "🎵 Audio MP3"])

quality = st.selectbox(
    "🎚 Chọn chất lượng video:",
    ["best", "720p", "480p", "360p"]
)

preview_btn = st.button("👀 Xem Preview")

download_btn = st.button("⬇️ Tải xuống")

# ===== LẤY INFO =====
def get_info(url):
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True
    }
    with YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

# ===== DOWNLOAD =====
def download_single(url, audio=False, quality="best"):
    if audio:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "audio.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
    else:
        fmt = {
            "best": "bestvideo+bestaudio/best",
            "720p": "bestvideo[height<=720]+bestaudio/best",
            "480p": "bestvideo[height<=480]+bestaudio/best",
            "360p": "bestvideo[height<=360]+bestaudio/best",
        }

        ydl_opts = {
            "format": fmt[quality],
            "outtmpl": "video.%(ext)s",
            "merge_output_format": "mp4"
        }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)

    return file


# ===== PREVIEW =====
if preview_btn and url:
    try:
        info = get_info(url)

        st.success("📺 Preview Video")

        if "entries" in info:  # playlist
            st.write("📂 Playlist detected:")
            for i, v in enumerate(info["entries"][:10]):
                st.write(f"{i+1}. {v.get('title')}")
        else:
            st.video(url)
            st.write("🎬 Title:", info.get("title"))

    except Exception as e:
        st.error(e)


# ===== DOWNLOAD =====
if download_btn and url:
    try:
        st.info("⏳ Đang xử lý...")

        info = get_info(url)

        # ===== PLAYLIST =====
        if "entries" in info:
            st.write("📂 Đang tải playlist...")

            for i, video in enumerate(info["entries"]):
                video_url = f"https://www.youtube.com/watch?v={video['id']}"

                st.write(f"⬇️ Download: {video.get('title')}")

                file = download_single(
                    video_url,
                    audio=(mode == "🎵 Audio MP3"),
                    quality=quality
                )

                with open(file, "rb") as f:
                    st.download_button(
                        f"📥 Tải {video.get('title')}",
                        data=f,
                        file_name=os.path.basename(file),
                        mime="video/mp4" if mode != "🎵 Audio MP3" else "audio/mpeg"
                    )

                os.remove(file)

        # ===== SINGLE VIDEO =====
        else:
            file = download_single(
                url,
                audio=(mode == "🎵 Audio MP3"),
                quality=quality
            )

            st.success("✅ Xong!")

            mime = "video/mp4" if mode != "🎵 Audio MP3" else "audio/mpeg"

            with open(file, "rb") as f:
                st.download_button(
                    "📥 Tải về máy",
                    data=f,
                    file_name=os.path.basename(file),
                    mime=mime
                )

            os.remove(file)

    except Exception as e:
        st.error(f"❌ Lỗi: {e}")