# frame_slicer_settings.py

import gradio as gr

# Default settings
frame_slicer_config = {
    "slice_size": 6,
    "estimated_time_per_slice": 20,
    "auto_detect": True
}

def frame_slicer_settings_interface():
    with gr.Blocks() as settings_ui:
        gr.Markdown("## ⚙️ Frame Slicer Settings")

        slice_input = gr.Number(label="Frame Slice Size (seconds)", value=frame_slicer_config["slice_size"])
        time_per_slice_input = gr.Number(label="Estimated Time per Slice (seconds)", value=frame_slicer_config["estimated_time_per_slice"])
        auto_detect_toggle = gr.Checkbox(label="Enable Auto-Detection", value=frame_slicer_config["auto_detect"])
        save_button = gr.Button("Save Settings")
        status_display = gr.Textbox(label="Status", interactive=False)

        def save_settings(slice_size, time_per_slice, auto_detect):
            frame_slicer_config["slice_size"] = slice_size
            frame_slicer_config["estimated_time_per_slice"] = time_per_slice
            frame_slicer_config["auto_detect"] = auto_detect
            return f"Settings updated: Slice Size = {slice_size}s, Time per Slice = {time_per_slice}s, Auto-Detect = {auto_detect}"

        save_button.click(save_settings, [slice_input, time_per_slice_input, auto_detect_toggle], status_display)

    return settings_ui

def get_frame_slicer_settings():
    return frame_slicer_config
