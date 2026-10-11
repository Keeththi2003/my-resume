# Resume

[![Build](https://img.shields.io/github/actions/workflow/status/Keeththi2003/my-resume/build.yaml?branch=main\&label=Build)](../../actions)
[![Release](https://img.shields.io/github/v/release/Keeththi2003/my-resume?label=Latest%20Release)](../../releases/latest)
![Visitors](https://visitor-badge.laobi.icu/badge?page_id=Keeththi2003.my-resume)
[![Downloads](https://img.shields.io/github/downloads/Keeththi2003/my-resume/total?label=Downloads)](../../releases)

Source code for my professional resume, built with **RenderCV** and automatically published using **GitHub Actions** and **GitHub Releases**.

---

## Latest Release

One resume per job role.

| Role                  | PDF                                                                    | HTML                                                                    |
| :-------------------- | :--------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| **Software Engineer** | **[Download](../../releases/latest/download/Keeththigan-SE.pdf)**           | **[View](../../releases/latest/download/Keeththigan-SE.html)**               |
| **Backend Engineer**  | **[Download](../../releases/latest/download/Keeththigan-Backend.pdf)**      | **[View](../../releases/latest/download/Keeththigan-Backend.html)**          |
| **DevOps Engineer**   | **[Download](../../releases/latest/download/Keeththigan-DevOps.pdf)**       | **[View](../../releases/latest/download/Keeththigan-DevOps.html)**           |
| **Mobile Developer**  | **[Download](../../releases/latest/download/Keeththigan-Mobile.pdf)**       | **[View](../../releases/latest/download/Keeththigan-Mobile.html)**           |

**[All Releases](../../releases)**

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

Generate one RenderCV file per role (`rendercv/cv.<role>.generated.yaml`).

```bash
python scripts/generate.py
```

Build every role.

```bash
scripts/build.sh
```

The generated files are written to `rendercv/rendercv_output/` as `Keeththigan-<Role>.pdf`, `.html` and `.md`.

---

## Layout

```text
rendercv/
  locale.yaml, settings.yaml, design.yaml   shared RenderCV settings
  base.yaml        name, contacts, education, experience, activities, skills
  projects/        one file per project
  variants/        one file per role: se, backend, devops, mobile
```

A variant file only holds what differs for that role:

```yaml
output_name: DevOps            # output becomes Keeththigan-DevOps.pdf
headline: ...
summary:
  - ...
projects:                      # project file names, in order
  - project1
  - project2
skills_order:                  # skills group labels from base.yaml, in order
  - Cloud & DevOps
  - Languages
highlight_sets:                # optional
  projects:
    project1: devops          # use highlights_devops from projects/<project_name>.yaml
  experience:
    company1: devops          # use highlights_devops from the entry with id: company1
```

If an entry has no list for the requested set, its normal `highlights` are used.


## Adding a Project

1. Create `rendercv/projects/<name>.yaml` with the usual RenderCV entry fields (`name`, `start_date`, `end_date`, `summary`, `highlights`, ...).
2. Optionally add alternative lists such as `highlights_mobile`.
3. Add `<name>` to the `projects` list of each variant that should show it.

## Adding a Role

1. Copy an existing file in `rendercv/variants/`, e.g. `cp rendercv/variants/backend.yaml rendercv/variants/frontend.yaml`.
2. Set `output_name`, `headline`, `summary`, `projects` and `skills_order`.
3. Run `python scripts/generate.py` and `scripts/build.sh`; the new role is built as `Keeththigan-<output_name>.pdf` and is uploaded by the release workflow automatically.
4. Add a download row for it to the table above.

---
