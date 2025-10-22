import os, time, requests

ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")
USER_ID = os.getenv("IG_USER_ID")

def post_image(image_url: str, caption: str) -> bool:
    if not (ACCESS_TOKEN and USER_ID):
        print("[instagram] Missing IG_ACCESS_TOKEN or IG_USER_ID; skipping.")
        return False
    try:
        create_url = f"https://graph.facebook.com/v20.0/{USER_ID}/media"
        r1 = requests.post(create_url, data={
            "image_url": image_url,
            "caption": caption,
            "access_token": ACCESS_TOKEN
        }, timeout=30)
        if not r1.ok:
            print("Create container failed:", r1.text); return False
        container_id = r1.json().get("id")
        time.sleep(2)
        publish_url = f"https://graph.facebook.com/v20.0/{USER_ID}/media_publish"
        r2 = requests.post(publish_url, data={
            "creation_id": container_id,
            "access_token": ACCESS_TOKEN
        }, timeout=30)
        if not r2.ok:
            print("Publish failed:", r2.text); return False
        print("[instagram] Post published:", r2.json()); return True
    except Exception as e:
        print("IG error:", e); return False
