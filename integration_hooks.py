# integration_hooks.py - Connect project_manager with system modules

import os
import gradio as gr
from project_manager import save_project, load_project, list_saved_projects

# You may connect these with any Gradio app or Blocks interface as needed
def add_project_management_ui(blocks_scope, project_state_getter, project_state_setter):
    with blocks_scope:
        gr.Markdown("## 💾 Project Save / Load Manager")

        with gr.Row():
            project_name_input = gr.Textbox(label="📁 Project Name (new or existing)")
            save_button = gr.Button("💾 Save Project")
            load_button = gr.Button("📂 Load Project")

        project_dropdown = gr.Dropdown(label="📜 Existing Projects", choices=list_saved_projects())
        message_output = gr.Textbox(label="📝 Status Message", interactive=False)

        def handle_save(name):
            if not name.strip():
                return "⚠️ Please enter a valid project name."
            state = project_state_getter()
            return save_project(name.strip(), state)

        def handle_load(name):
            if not name.strip():
                return "⚠️ Please enter a valid project name."
            state = load_project(name.strip())
            if state:
                project_state_setter(state)
                return f"✅ Project '{name}' loaded."
            return f"❌ Failed to load project '{name}'."

        save_button.click(handle_save, inputs=project_name_input, outputs=message_output)
        load_button.click(handle_load, inputs=project_name_input, outputs=message_output)
        project_dropdown.change(fn=project_name_input.update, inputs=project_dropdown)

        return message_output
