import requests
import yt_dlp
import os

TOKEN = '8500122217:AAFruJrJOFSVHmRRIS3hgKUPSMKAxNHVp70'
CHAT_ID = '8511545567'
CHANNELS = [
    'UCjoXvuLqgM9UB_7Mn-pJ2PA',
    'UC2VbnGvLPVeiBKSs2gCkpcA',
    'UCxBXVH3DxjFHoqrR607CrOg',
    'UCgOBjBoCTR5uMcIK23sj1pw'
]

def check_channels():
    for c_id in CHANNELS:
        url = f"https://www.youtube.com/channel/{c_id}/videos"
        try:
            ydl_opts = {'quiet': True, 'extract_flat': True, 'force_generic_extractor': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info and len(info['entries']) > 0:
                    video = info['entries'][0]
                    v_id = video['id']
                    
                    file_path = f"{c_id}.txt"
                    last_id = ""
                    if os.path.exists(file_path):
                        with open(file_path, "r") as f: last_id = f.read().strip()
                    
                    if v_id != last_id:
                        msg = f"<b>🎬 محتوى جديد نزل!</b>\n\n<b>📝 العنوان:</b> {video['title']}\n\nhttps://www.youtube.com/watch?v={v_id}"
                        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"})
                        with open(file_path, "w") as f: f.write(v_id)
        except Exception as e:
            print(f"Error checking {c_id}: {e}")

if __name__ == "__main__":
    check_channels()
