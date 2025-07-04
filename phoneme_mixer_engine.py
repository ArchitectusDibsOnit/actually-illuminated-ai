# phoneme_mixer_engine.py

import gradio as gr

phoneme_timeline = []

def phoneme_replacement_interface():
    gr.Markdown("## 📝 Phoneme Replacement Engine")

    with gr.Row():
        phoneme_log = gr.Textbox(label="Phoneme Timeline Log", lines=10, interactive=False)

    with gr.Row():
        selected_voice = gr.Textbox(label="Voice Name")
        phoneme_time = gr.Number(label="Phoneme Time (seconds)", value=0)
        original_phoneme = gr.Textbox(label="Original Phoneme")
        replacement_phoneme = gr.Textbox(label="Replacement Phoneme")

    replace_button = gr.Button("Replace Phoneme")

    def replace_phoneme(voice, time, original, replacement):
        entry = {
            'voice': voice,
            'time': time,
            'original_phoneme': original,
            'replacement': replacement
        }
        phoneme_timeline.append(entry)
        log_entries = [f"{e['time']}s: {e['voice']} - {e['original_phoneme']} ➜ {e['replacement']}" for e in phoneme_timeline]
        return "\n".join(log_entries)

    replace_button.click(
        replace_phoneme,
        inputs=[selected_voice, phoneme_time, original_phoneme, replacement_phoneme],
        outputs=phoneme_log
    )

    return gr.Column([
        phoneme_log,
        selected_voice,
        phoneme_time,
        original_phoneme,
        replacement_phoneme,
        replace_button
    ])
