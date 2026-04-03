import typer
from texcv.renderer import render_cv

app = typer.Typer()

@app.command()
def run(input_file: str, output: str = "cv.tex"):
    render_cv(input_file, output)
    print(f"Generated: {output}")