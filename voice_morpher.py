# voice_morpher.py

import gradio as gr

def voice_morpher_interface():
    with gr.Blocks() as morpher_ui:
        gr.Markdown("## 🎛️ Voice Morpher")

        with gr.Row():
            audio_input = gr.Audio(source="upload", label="Upload Voice Clip")
            pitch_shift_input = gr.Slider(minimum=-12, maximum=12, value=0, step=1, label="Pitch Shift (semitones)")
            speed_input = gr.Slider(minimum=0.5, maximum=2.0, value=1.0, step=0.1, label="Speed Multiplier")

        process_button = gr.Button("Morph Voice")
        morphed_audio_output = gr.Audio(label="Morphed Voice Output", interactive=False)

        def morph_voice(audio, pitch_shift_value, speed_value):
            if audio is None:
                return None

            from audio_utils import pitch_shift, time_stretch, load_audio, save_audio
            import os
            import torch

            temp_path = audio
            waveform, sr = load_audio(temp_path)

            morphed_waveform = pitch_shift(waveform, sr, pitch_shift_value)
            morphed_waveform = time_stretch(morphed_waveform, sr, speed_value)

            output_path = "morphed_voice.wav"
            save_audio(output_path, morphed_waveform, sr)
            return output_path

        process_button.click(
            fn=morph_voice,
            inputs=[audio_input, pitch_shift_input, speed_input],
            outputs=morphed_audio_output
        )

    return morpher_ui
