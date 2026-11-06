# CV — Vũ Hữu Đô (Vu Huu Do)

Bộ CV đa phiên bản cho **Vũ Hữu Đô** — Full Stack Developer (.NET / React), TP. Hồ Chí Minh.
Nội dung được viết một lần, sinh ra nhiều bản theo **role** và **định dạng** (ATS / visual, EN / VI).

## Nộp ở đâu — dùng file nào

| Ứng tuyển vị trí | Tiếng Anh (ATS) | Tiếng Việt |
|---|---|---|
| Full Stack Developer (.NET / React) | `cv/fullstack/CV_VuHuuDo_FullStack_EN_ATS.pdf` | `cv/fullstack/CV_VuHuuDo_FullStack_VI_Visual.pdf` |
| Software Engineer (tổng quát) | `cv/software-engineer/CV_VuHuuDo_SoftwareEngineer_EN_ATS.pdf` | `cv/software-engineer/CV_VuHuuDo_SoftwareEngineer_VI_Visual.pdf` |
| Backend Developer (.NET / C#) | `cv/backend-dotnet/CV_VuHuuDo_BackendDotNet_EN_ATS.pdf` | `cv/backend-dotnet/CV_VuHuuDo_BackendDotNet_VI_Visual.pdf` |
| Frontend Developer (React / TS) | `cv/frontend-react/CV_VuHuuDo_FrontendReact_EN_ATS.pdf` | `cv/frontend-react/CV_VuHuuDo_FrontendReact_VI_Visual.pdf` |
| DevOps Engineer | `cv/devops/CV_VuHuuDo_DevOps_EN_ATS.pdf` | `cv/devops/CV_VuHuuDo_DevOps_VI_Visual.pdf` |
| AI & Automation Engineer | `cv/ai-automation/CV_VuHuuDo_AIAutomation_EN_ATS.pdf` | `cv/ai-automation/CV_VuHuuDo_AIAutomation_VI_Visual.pdf` |

- **`_EN_ATS.pdf`** — 1 cột, không ảnh/icon: an toàn khi nộp qua hệ thống tuyển dụng (ATS), LinkedIn, ITviec/TopCV.
- **`_VI_Visual.pdf`** — 2 cột, có ảnh: gửi email hoặc gặp trực tiếp nhà tuyển dụng Việt Nam.
- **`_EN_Visual.pdf`** — bản EN 2 cột, có ảnh: gửi email cho nhà tuyển dụng nước ngoài / người đọc tiếng Anh (có ở cả 6 role, vd: `cv/fullstack/CV_VuHuuDo_FullStack_EN_Visual.pdf`).
- **`cv/linkedin/CV_VuHuuDo_LinkedIn.pdf`** — bản export từ LinkedIn (tham chiếu).

## Web app (C# / Docker)

```bash
docker compose up -d --build     # http://localhost:8080
```

- Điền form, chọn role, tạo **2 loại CV 1 trang**: Human (2 cột, có ảnh) và ATS (1 cột, chữ thuần).
- Tải CV có sẵn lên (.pdf/.docx/.txt/.md) để trích nội dung và nhận góp ý: thiếu mục chuẩn, sáo ngữ, không có số liệu, từ cấm có thể lộ thông tin.
- Hồ sơ và PDF nằm ở `./data/` (mount vào container, không commit). File do container tạo thuộc
  `PUID:PGID` (mặc định `1000:1000` — đổi bằng `PUID=$(id -u) PGID=$(id -g) docker compose up -d`).
- Không gọi dịch vụ AI ngoài; toàn bộ chạy offline trong container.
- Image dùng `chrome-headless-shell` chính thức (cùng engine in PDF với Chrome, bỏ GTK/X11/DRM) và chỉ
  cài font Liberation — đủ dấu tiếng Việt; mỗi PDF sinh ra vẫn được đối chiếu text layer để bắt lỗi mất dấu.

API: `GET /api/health`, `GET/PUT /api/profiles/{id}`, `POST /api/render`, `POST /api/improve` (multipart).

## TUI + CLI (nhiều người dùng)

```bash
uv run cvtui.py                    # TUI: chọn hồ sơ, nhập role/JD, Ctrl+G tạo, Ctrl+S lưu
uv run cvtui.py --new <id>         # tạo hồ sơ từ profiles/_template
uv run cvtui.py --list
uv run cvtui.py --profile <id> --role "DevOps Engineer" --jd jd.txt --lang EN,VI \
    [--title "Senior DevOps"] [--name "..."] [--avatar ~/anh.jpg]
uv run cvtui.py --check
```

- Hồ sơ: `profiles/<id>/profile.json`. Hồ sơ mẫu `vuhuudo` dựng từ `content/` (chỉ đọc) — `--new` để tạo bản sửa được.
- `profiles/<id>/denylist.txt`: mỗi dòng một từ cấm; CV chứa từ này sẽ bị báo `RÒ RỈ` và lệnh trả mã 1.
- `profiles/*`, `denylist.txt`, `data/`, `out/` đều bị gitignore.

Hướng dẫn viết nội dung: [`docs/CV_GUIDE.md`](docs/CV_GUIDE.md). Quy trình cho AI agent: [`AGENTS.md`](AGENTS.md).

## Cấu trúc

```
├── README.md
├── build.sh                  # lệnh build duy nhất: ./build.sh
├── build.py                  # sinh HTML (build/out/) và PDF (cv/)
├── cvtui.py                  # TUI tạo CV theo role/JD đa người dùng (out/, không commit)
├── webapp/                   # Web app C# (.NET 10) + Dockerfile
├── docker-compose.yml        # docker compose up -d --build -> :8080
├── profiles/                 # hồ sơ người dùng (gitignore trừ _template)
├── content/                  # NGUỒN NỘI DUNG
│   ├── profile.py            #   thông tin chung: tên, liên hệ, học vấn, ngôn ngữ, nhãn mục
│   ├── bank.json             #   ngân hàng nội dung (kinh nghiệm, dự án, kỹ năng) cho cvtui.py
│   └── cvs/                  #   mỗi role một file
│       ├── fullstack.py
│       ├── software_engineer.py
│       ├── backend_dotnet.py
│       ├── frontend_react.py
│       ├── devops.py
│       └── ai_automation.py
├── templates/                # MẪU TRÌNH BÀY (HTML + CSS)
│   ├── ats.html              #   bản 1 cột, tối giản
│   └── visual.html           #   bản 2 cột, sidebar
├── assets/
│   ├── avatar.png            # ảnh dùng chung cho mọi bản
│   └── fonts/                # Liberation Sans nhúng sẵn — dấu tiếng Việt to, rõ ở mọi môi trường
├── cv/                       # ĐẦU RA — PDF đã build (commit sẵn để tải/gửi ngay)
├── build/                    # HTML tạm trong lúc build (không commit)
└── out/                      # CV sinh bởi cvtui.py (không commit)
```

## Build lại PDF

Yêu cầu: **Chromium** (hoặc Chrome) + **Python 3** (khuyến nghị **uv**; `pdfinfo` tuỳ chọn để kiểm tra số trang).
Script tự tìm Chrome theo thứ tự: biến `CHROME` → chromium/chrome trong PATH → Chromium của Playwright.

```bash
./build.sh          # tự dùng uv nếu có, không thì python3
uv run build.py     # hoặc chạy trực tiếp (PEP 723, không cần cài thêm gì)
python3 build.py
```

Script build toàn bộ, kiểm tra từng bản **vừa đúng 1 trang** và báo lỗi nếu không.

## TUI tạo CV theo role

```bash
uv run cvtui.py                                   # mở TUI: nhập role (+ dán JD) -> Ctrl+G
uv run cvtui.py --role "DevOps Engineer" --jd jd.txt --lang EN,VI   # không cần TUI
uv run cvtui.py --check                           # tự kiểm tra logic chọn nội dung
# tuỳ chỉnh: --name "Nguyen Van A" --title "Senior Backend Engineer" --avatar ~/anh.jpg
```

Mỗi lần ra 2 loại, 1 trang A4, lưu ở `out/<role>/` (không commit):
- `*_Human.pdf` — 2 cột, có ảnh, nộp cho người đọc.
- `*_ATS.pdf` — 1 cột, chữ thuần, nộp cho máy đọc.

Nội dung chọn từ `content/bank.json` (ngân hàng nội dung) theo độ khớp role/JD. Kỹ năng JD đòi mà bank chưa có chỉ được **báo thiếu**, không tự thêm vào CV. Muốn thêm kinh nghiệm/kỹ năng: sửa `content/bank.json` (viết chung chung, không nêu thông tin nội bộ).

## Chỉnh sửa nội dung

1. Sửa nội dung trong `content/cvs/<role>.py` (hoặc thông tin chung trong `content/profile.py`).
2. Chạy `./build.sh` — PDF trong `cv/` được cập nhật.
3. Commit cả nội dung lẫn PDF.

**Thêm role mới**: tạo `content/cvs/<role>.py` theo mẫu các file có sẵn, rồi thêm vào danh sách `CVS`
trong `content/cvs/__init__.py`.

## Ghi chú

- **Font nhúng sẵn**: `assets/fonts/` (Liberation Sans — chuẩn Arial; giấy phép: `assets/fonts/LICENSE-Liberation.txt`) — mọi renderer (build.py, cvtui, webapp/Docker) dùng đúng font này qua `@font-face`, không phụ thuộc font hệ thống; dấu tiếng Việt (ậ, ệ, ộ…) to, rõ ở mọi cỡ chữ.
- CV chỉ **mô tả chung** (không nêu tên hệ thống nội bộ, số liệu đơn vị, hạ tầng); repo công khai nên không thêm chi tiết nội bộ.
- LinkedIn: `linkedin.com/in/vuhuudo` — khai báo một chỗ trong `content/profile.py`, mọi bản CV tự lấy theo.
- Nội dung CV là thông tin cá nhân — vui lòng không dùng lại; mã build (`build.py`, `templates/`) tự do tham khảo.
