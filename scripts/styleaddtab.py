import modules.scripts as scripts
import gradio as gr
import os, pathlib, csv

from modules import script_callbacks


def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        
        with gr.Row():
            styleInput = gr.Textbox(
                label="Style CSV", lines=5, placeholder='styleName,"positive","negative"'
            )
        with gr.Row():
            output = gr.components.Text(label="Output")
            button: gr.Button = gr.Button(label="Add Style")
        button.click(
            fn=addStyle,
            inputs=[styleInput],
            outputs=[output]
        )
        return [(ui_component, "yoinked style adder", "yoinked_style_tab")]
def addStyle(styletxt):
    #verify if the csv is valid
    valid, styletxt = VerifyCSV(styletxt)
    if not valid:
        return styletxt
    path = pathlib.Path(__file__).parent.absolute()
    path = path.parent.absolute()
    path = path.parent.absolute()  #hello os.path users
    path = path.parent.absolute() 
    #now that we have the path, we can open the file
    with open(path.joinpath("styles.csv"), "a", encoding="utf-8") as f:
        for obj in styletxt.split("\n"):
            f.write("\n")
            f.write(obj)
    #double \n handling
    data = ""
    with open(path.joinpath("styles.csv"), "r", encoding="utf-8") as f:
        data = f.read()
    data = data.replace("\n\n", "\n")
    with open(path.joinpath("styles.csv"), "w", encoding="utf-8") as f:
        f.write(data)
    if len(styletxt.split("\n")) == 1:
        return "Style added successfully!"
    return "Styles added successfully!" #small detail


def VerifyCSV(val):
    goodRow = []
    val.replace(",\n", "\n")
    try:
        rows = csv.reader(val.splitlines())
        for row in rows:
            if len(row) != 3:
                pass #do nothing
            else:
                goodRow.append(row)
    except csv.Error:
        return False, "CSV string is not a valid CSV"
    if not goodRow:
        return False, "CSV does not have any good rows"
    x = ""
    for n in goodRow:
        x += f'{n[0]},"{n[1]}","{n[2]}"\n' #yeah...
    return True, x

script_callbacks.on_ui_tabs(on_ui_tabs)
