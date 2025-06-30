# lyric_timing_overlay.py

def generate_lyric_timeline_overlay(timeline_log):
    overlay = []
    for entry in timeline_log:
        overlay.append(f"[{entry['start_time']}s - {entry['end_time']}s] {entry['voice']}: {entry['lyrics']}")
    return "\n".join(overlay)
