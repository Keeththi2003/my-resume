# Resume

[![Build](https://img.shields.io/github/actions/workflow/status/<your-username>/resume/build.yml?branch=main\&label=Build)](../../actions)
[![Release](https://img.shields.io/github/v/release/<your-username>/resume?label=Latest%20Release)](../../releases/latest)
[![License](https://img.shields.io/github/license/<your-username>/resume)](LICENSE)

Source code for my professional resume, built with **RenderCV** and automatically published using **GitHub Actions** and **GitHub Releases**.

---

## Latest Release

| Format              | Download                                                                |
| :------------------ | :---------------------------------------------------------------------- |
| **PDF**             | **[Download Latest Resume](../../releases/latest/download/Resume.pdf)** |
| **HTML**            | **[View Latest Resume](../../releases/latest/download/Resume.html)**    |
| **Release History** | **[All Releases](../../releases)**                                      |

---

## Tech Stack

* RenderCV
* Python
* GitHub Actions
* GitHub Releases

---

## Local Build

Install dependencies.

```bash
python -m pip install --upgrade pip
pip install "rendercv[full]"
pip install -r requirements.txt
```

Generate the RenderCV configuration.

```bash
python scripts/generate.py
```

Build the resume.

```bash
cd rendercv
rendercv render cv.generated.yaml
```

The generated files are written to:

```text
rendercv/rendercv_output/
```

---
