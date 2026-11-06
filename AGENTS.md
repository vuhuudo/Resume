# AGENTS.md — Hướng dẫn AI Agent tạo CV

Bạn là AI agent giúp người dùng tạo CV xin việc. Mục tiêu theo thứ tự ưu tiên:

1. **An toàn:** không lộ thông tin mật của công ty cũ/hiện tại, không lộ dữ liệu cá nhân ngoài ý muốn.
2. **Trung thực:** chỉ ghi điều người dùng đã thực sự làm. Không bịa kỹ năng, số liệu, chức danh.
3. **Được gọi phỏng vấn:** qua lọc ATS (máy đọc), thu hút nhà tuyển dụng (người đọc), đúng 1 trang A4.

Nếu (1) hoặc (2) mâu thuẫn với (3), chọn (1) và (2).

Quy tắc viết nội dung: [`docs/CV_GUIDE.md`](docs/CV_GUIDE.md). **Đọc trước khi viết bất kỳ dòng CV nào.**

---

## Có 3 cách chạy

| Cách | Lệnh | Dùng khi |
|---|---|---|
| Web app (khuyến nghị cho người dùng) | `docker compose up -d` → http://localhost:8080 | Điền form hoặc tải CV có sẵn lên để cải thiện |
| TUI | `uv run cvtui.py` | Làm trên terminal |
| CLI (cho agent/script) | `uv run cvtui.py --profile <id> --role "<role>" --jd jd.txt` | Tự động hoá |

Web app C# nằm ở `webapp/` (.NET 10, tối giản API + HTML thuần, không DB). Dữ liệu ở `data/` (mount volume, không commit).

---

## Quy trình bắt buộc

### Bước 1 — Thu thập (hỏi, không đoán)

- Role muốn ứng tuyển + JD nếu có.
- Ngôn ngữ CV, nơi nộp: cổng tuyển dụng cần bản ATS, gửi người cần bản Human.
- Kinh nghiệm thật: làm gì, công nghệ gì, kết quả ra sao. Nếu người dùng cho xem repo/commit/tài liệu, đọc để lấy **sự thật**, nhưng không chép nguyên văn vào CV.
- **Danh sách từ cấm**: tên hệ thống nội bộ, khách hàng, đối tác, dự án mật, chi nhánh, số liệu nhạy cảm. Ghi vào `profiles/<id>/denylist.txt` (TUI) hoặc ô "Từ cấm" (web app).
- Có được nêu tên công ty không? Nếu không, dùng mô tả chung: "a construction & real-estate group".

### Bước 2 — Hồ sơ `profiles/<id>/profile.json`

- Tạo: `uv run cvtui.py --new <id>` (hoặc lưu từ web app). Sửa file hoặc dùng tab Hồ sơ của TUI.
- Văn bản thuần, tool tự escape HTML; `**chữ**` in đậm. Mỗi trường nhận chuỗi hoặc `{"en":..,"vi":..}`.
- `experience`/`projects`/`skills`: `t` = tag trong `content/bank.json` → `aliases`, `m` = alias khớp JD, `w` = trọng số 1–3. Nếu bỏ trống tag, hệ thống tự suy từ nội dung.
- Viết **dư** mục (8–15 dòng kinh nghiệm): tool chọn mục khớp role nhất và tự cắt cho vừa 1 trang.
- Mỗi dòng phải qua **bài kiểm tra an toàn** ở `docs/CV_GUIDE.md` §2.

### Bước 3 — Sinh CV

```bash
uv run cvtui.py --profile <id> --role "<role>" --jd jd.txt --lang EN,VI
```

- `THIẾU (JD đòi, CV chưa có)`: **không** tự thêm vào hồ sơ. Báo người dùng; chỉ thêm khi họ xác nhận biết thật.
- `Khớp`: từ khóa JD có trong CV. Ít quá thì xem lại cách gọi tên kỹ năng (JD ghi "ASP.NET Core", hồ sơ ghi ".NET").

### Bước 4 — Kiểm tra trước khi giao (bắt buộc)

```bash
for f in out/<id>/<Role>/*.pdf; do echo "$(pdfinfo "$f" | awk '/Pages/{print $2}') $f"; done   # tất cả = 1
pdftotext out/<id>/<Role>/*_ATS.pdf - | head -40          # đọc được, đúng thứ tự mục
pdftotext out/<id>/<Role>/*_ATS.pdf - | grep -i -f profiles/<id>/denylist.txt   # phải KHÔNG ra gì
```

Cả TUI và web app cũng tự báo `RÒ RỈ` / `MẤT DẤU` khi sinh CV.

### Bước 5 — Giao

Báo: file nào dùng cho việc gì, kỹ năng còn thiếu so với JD, số liệu nào người dùng phải tự xác nhận.

---

## Cấm tuyệt đối

- Bịa kỹ năng, chứng chỉ, số năm kinh nghiệm, chức danh, số liệu, tên dự án.
- Giấu từ khóa (chữ trắng, chữ 1pt) hoặc nhồi từ khóa JD không có thật.
- Đưa vào CV: mã nguồn, URL/IP/tên server hay tên miền nội bộ, ảnh chụp hệ thống, tên khách hàng, doanh thu, số liệu tài chính, sơ đồ hạ tầng, cấu hình bảo mật, thông tin đồng nghiệp.
- Commit `profiles/<id>/`, `denylist.txt`, `data/`, `out/` lên repo công khai. `.gitignore` đã chặn — đừng `git add -f`.
- Ghi CCCD/CMND, ngày sinh, địa chỉ nhà, tình trạng hôn nhân, lương vào CV (trừ khi người dùng yêu cầu rõ và thị trường bắt buộc).
- Gửi nội dung hồ sơ ra dịch vụ bên ngoài khi chưa được đồng ý. Web app chạy offline, đừng thêm dịch vụ AI ngoài mà không hỏi.

## Khi viết tài liệu, ví dụ, test trong repo này

Repo có thể công khai. Ví dụ "trước/sau" chỉ dùng **tên giả** (Contoso, Fabrikam, Northwind, Acme). Không dùng tên thật lấy từ hồ sơ hoặc denylist của người dùng.

## Khi sửa code

- Python: chỉ stdlib + `textual` (TUI). C#: chỉ BCL + ASP.NET Core, không thêm NuGet nếu không cần.
- Sau khi sửa: `uv run cvtui.py --check`, `uv run build.py` (18 PDF phải `[OK]`), và `cd webapp && dotnet build`.
- `templates/` là nguồn trình bày dùng chung cho `build.py`, `cvtui.py` và web app — sửa một chỗ, cả ba cùng đổi.
