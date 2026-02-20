import requests
import time
import yt_dlp
import sys

# --- إعداداتك الخاصة ---
TOKEN = '8500122217:AAFruJrJOFSVHmRRIS3hgKUPSMKAxNHVp70'
CHAT_ID = '8511545567'

CHANNELS = [
    'https://www.youtube.com/channel/UCjoXvuLqgM9UB_7Mn-pJ2PA',
    'https://www.youtube.com/channel/UC2VbnGvLPVeiBKSs2gCkpcA',
    'https://www.youtube.com/channel/UCxBXVH3DxjFHoqrR607CrOg',
    'https://www.youtube.com/channel/UCgOBjBoCTR5uMcIK23sj1pw'
]

last_videos = {}

def get_last_video(channel_url):
    try:
        ydl_opts = {'quiet': True, 'extract_flat': True, 'force_generic_extractor': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"{channel_url}/videos", download=False)
            if 'entries' in result and len(result['entries']) > 0:
                return result['entries'][0]
    except Exception as e:
        print(f"خطأ: {e}")
    return None

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, json=payload)

print("🚀 البوت انطلق...")

# لتجنب إرسال فيديوهات قديمة عند التشغيل
for url in CHANNELS:
    video = get_last_video(url)
    if video: last_videos[url] = video['id']

while True:
    for url in CHANNELS:
        video = get_last_video(url)
        if video:
            v_id = video['id']
            if url in last_videos and last_videos[url] != v_id:
                msg = f"<b>🎬 فيديو جديد!</b>\n\n<b>📝 العنوان:</b> {video.get('title')}\n\n🔗 https://www.youtube.com/watch?v={v_id}"
                send_telegram(msg)
            last_videos[url] = v_id
    time.sleep(300) # فحص كل 5 دقائق
