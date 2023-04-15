import modules.scripts as scripts
import gradio as gr
import csv
from pathlib import Path
from modules.paths import script_path
from modules import script_callbacks, paths
def refresh():
    csvpath = Path(script_path)
    with open(csvpath.joinpath("styles.csv"), "r", encoding="utf-8") as f:
        data = f.read()
    goods = []
    rows = csv.reader(data.splitlines())
    for row in rows:
        if len(row) != 3:
            pass #do nothing
        else:
            goods.append(row)
    styles = []
    for n in goods:
        if "name" in n[0]:
            continue
        styles.append(n[0])
    return styles
styles = refresh()
def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        with gr.Tab("Add/Import"):
            with gr.Row():
                astyleInput = gr.Textbox(
                    label="Style CSV", lines=5, placeholder='styleName,"positive","negative"'
                )
            with gr.Row():
                aoutput = gr.components.Text(label="Output")
                abutton: gr.Button = gr.Button("Add Style")
            abutton.click(
                fn=addStyle,
                inputs=[astyleInput],
                outputs=[aoutput]
            )
        with gr.Tab("Export/Delete"):
            with gr.Row():
                edropdown = gr.Dropdown(label="Style", choices=styles)
                erefresh = gr.Button("Refresh")
                eoutput = gr.components.Text(label="Output")
                eaction = gr.Dropdown(label="Action", choices=["export", "delete"])
            erefresh.click(
                fn=lambda: edropdown.update(choices=refresh()), #i punched a wall to make this code work
                outputs=[edropdown]
            )

            with gr.Row():
                edata = gr.components.Text(label="Data", lines=7)
            with gr.Row():
                ebutton: gr.Button = gr.Button("Do action")
            ebutton.click(
                fn=actionIze,
                inputs=[edropdown, eaction],
                outputs=[edata, eoutput]
            )
        return [(ui_component, "yoinked style manager", "yoinked_style_tab")]
def addStyle(styletxt):
    #verify if the csv is valid
    valid, styletxt = VerifyCSV(styletxt)
    if not valid:
        return styletxt
    path = Path(script_path) #so from /webui/extensions/yoinked-style-adder/scripts/ to /webui/
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
def actionIze(style, action):
    #open the csv
    path = Path(script_path)
    with open(path.joinpath("styles.csv"), "r", encoding="utf-8") as f:
        data = f.read()
    #read
    rows = csv.reader(data.splitlines())
    roz = []
    for row in rows:

        if len(row) != 3:
            ...
        else:
            if row[0] == style:
                if action == "export":
                    return  f'{row[0]},"{row[1]}","{row[2]}"', "Copy the data below and send it to share!"
                elif action == "delete":
                    pass
        roz.append(row)
    if action == "export":
        return "", "Couldnt find the style in the csv, try pressing the refresh button"
    elif action == "delete":
        #for each line in data, if it starts with the style, delete it
        validation = False
        for row in data.splitlines():
            if row.startswith(f"{style},"):
                data = data.replace(row, "")
                validation = True
        if not validation:
            return "", "Couldnt find the style in the csv, try pressing the refresh button"
        data.replace("\n\n", "\n")
        with open(path.joinpath("styles.csv"), "w", encoding="utf-8") as f:
            f.write(data)
        return "", "Style deleted successfully!"
    else:
        return "", "Invalid action"
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
