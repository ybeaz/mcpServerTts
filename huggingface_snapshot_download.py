from huggingface_hub import snapshot_download


REPO_ID = "coqui/XTTS-v2"
LOCAL_DIR = "./assets/xtts_v2"

print("⏳ ",REPO_ID, " downloading starts... ")

snapshot_download(
    repo_id=REPO_ID,
    local_dir=LOCAL_DIR,
)

print("✅ ",LOCAL_DIR, " done → ", LOCAL_DIR)

'''
  Terminal > `python huggingface_snapshot_download.py`
'''