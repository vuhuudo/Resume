#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = ["textual>=0.80"]
# ///
"""TUI tạo CV theo role (và JD nếu có) cho nhiều người dùng.

Mỗi lần ra 2 loại CV, 1 trang A4:
  - Human: 2 cột, có ảnh, nộp cho người đọc.
  - ATS  : 1 cột, chữ thuần, nộp cho máy đọc.
Nội dung chọn từ profiles/<id>/profile.json theo độ khớp với role/JD.
Không bịa kỹ năng: thứ JD đòi mà hồ sơ không có chỉ được báo là "thiếu".

  uv run cvtui.py                            # mở TUI
  uv run cvtui.py --list | --new <id>        # danh sách / tạo hồ sơ từ mẫu
  uv run cvtui.py --profile <id> --role "DevOps" [--jd jd.txt] [--lang EN,VI]
  uv run cvtui.py --check                    # tự kiểm tra
"""
import argparse
import html
import json
import os
import re
import shutil
import sys
import unicodedata
from types import SimpleNamespace
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B                       # noqa: E402
from content import profile as builtin  # noqa: E402

ROOT = B.ROOT
OUT = os.path.join(ROOT, "out")
PROFILES = os.path.join(ROOT, "profiles")
BANK = json.load(open(os.path.join(ROOT, "content", "bank.json"), encoding="utf-8"))
TAX = {"aliases": BANK["aliases"], "watchlist": BANK["watchlist"]}
LIMITS = dict(exp=7, proj=3, group_items=8, groups=7)
STYLE = {"human": "visual", "ats": "ats"}
REQUIRED = ("name", "job", "education", "languages", "summary",
            "experience", "projects", "skills")
P = None          # hồ sơ đang dùng (dict), đặt bởi use_profile()
PERSON = None     # SimpleNamespace cho build.build_html


# ------------------------------------------------------------------ hồ sơ ---
def list_profiles():
    return sorted(d for d in os.listdir(PROFILES)
                  if d != "_template" and os.path.isfile(os.path.join(PROFILES, d, "profile.json")))


def _builtin_profile():
    """Hồ sơ "vuhuudo" dựng từ content/profile.py + content/bank.json (chỉ đọc)."""
    b = BANK
    return {
        "_id": "vuhuudo", "_dir": os.path.join(ROOT, "content"), "_readonly": True,
        "name": dict(builtin.NAME),
        "avatar": "../assets/avatar.png",
        "contact_line": dict(builtin.CONTACT_LINE),
        "contacts": {k: [list(c) for c in v] for k, v in builtin.CONTACT_ITEMS.items()},
        "job": {k: dict(v) for k, v in builtin.JOB.items()},
        "education": {k: dict(v) for k, v in builtin.EDUCATION.items()},
        "languages": {k: dict(v) for k, v in builtin.LANGUAGES.items()},
        "availability": dict(builtin.AVAILABILITY),
        "years": b.get("years", {"en": "1.5", "vi": "1,5"}),
        "summary": {
            "en": ("{title} with {years} years of experience building and operating enterprise web "
                   "platforms. Hands-on with {skills}. Delivered reporting, authentication and data "
                   "platforms to production."),
            "vi": ("{title} với {years} năm kinh nghiệm xây dựng và vận hành nền tảng web doanh "
                   "nghiệp. Thực chiến với {skills}. Đã đưa nền tảng báo cáo, xác thực và dữ liệu "
                   "lên production."),
        },
        "experience": b["experience"], "projects": b["projects"], "skills": b["skills"],
    }


def use_profile(ref):
    """ref = id trong profiles/ hoặc đường dẫn tới profile.json. '' = hồ sơ mẫu dựng từ content/."""
    global P, PERSON
    if not ref or ref == "vuhuudo":
        P = _builtin_profile()
        PERSON = _person(P)
        return P
    path = ref if os.path.exists(ref) else os.path.join(PROFILES, ref)
    path = os.path.join(path, "profile.json") if os.path.isdir(path) else path
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Không thấy hồ sơ '{ref}'. Có: {', '.join(list_profiles()) or '(chưa có)'}")
    P = json.load(open(path, encoding="utf-8"))
    P["_dir"] = os.path.dirname(os.path.abspath(path))
    P["_id"] = os.path.basename(os.path.dirname(os.path.abspath(path)))
    P.pop("_readonly", None)
    miss = [k for k in REQUIRED if k not in P]
    if miss:
        raise ValueError(f"Hồ sơ thiếu mục: {', '.join(miss)} (xem profiles/_template/profile.json)")
    PERSON = _person(P)
    return P


def save_profile(data=None):
    """Ghi hồ sơ đang dùng ra profiles/<id>/profile.json. Không ghi đè hồ sơ chỉ đọc."""
    if P.get("_readonly"):
        raise PermissionError(f"Hồ sơ '{P['_id']}' là hồ sơ mẫu trong content/, chỉ đọc. "
                              "Dùng --new <id> rồi sửa bản sao.")
    data = data or P
    clean = {k: v for k, v in data.items() if not k.startswith("_")}
    path = os.path.join(P["_dir"], "profile.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(clean, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return path


def new_profile(pid):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", pid) or pid in ("_template", "vuhuudo"):
        raise ValueError("id chỉ gồm chữ, số, - và _ (không dùng 'vuhuudo' / '_template')")
    dst = os.path.join(PROFILES, pid)
    if os.path.exists(dst):
        raise FileExistsError(f"Đã có profiles/{pid}")
    shutil.copytree(os.path.join(PROFILES, "_template"), dst)
    return os.path.join(dst, "profile.json")


def _person(p):
    """dict hồ sơ -> đối tượng giống content.profile cho build.build_html."""
    return SimpleNamespace(
        NAME=p["name"], CONTACT_LINE=p["contact_line"], CONTACT_ITEMS=p["contacts"],
        JOB=p["job"], EDUCATION=p["education"], LANGUAGES=p["languages"],
        AVAILABILITY=p.get("availability", {}),
        LABELS=builtin.LABELS, icon=builtin.icon,
    )


# ------------------------------------------------------------- nội dung -----
def tx(v, lang):
    """Chuỗi hoặc {en,vi} -> chuỗi (thiếu ngôn ngữ thì lấy en)."""
    if isinstance(v, dict) and ("en" in v or "vi" in v):
        return v.get(lang, v.get("en", ""))
    return v


def esc(text):
    """Văn bản thuần -> HTML an toàn; **x** -> <b>x</b>."""
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(str(text), quote=False))


def has(text, word):
    return re.search(r"(?<![\w])" + re.escape(word) + r"(?![\w])", text) is not None


def analyze(role, jd=""):
    role_l, jd_l = role.lower(), jd.lower()
    both = role_l + "\n" + jd_l
    tags = {}
    for tag, words in TAX["aliases"].items():
        n = sum(3 * has(role_l, w) + min(2, jd_l.count(w)) * has(jd_l, w) for w in words)
        if n:
            tags[tag] = n
    if not tags:
        tags = {"fullstack": 3}
    matched, known = [], set()
    for g in P["skills"]:
        for it in g["items"]:
            ms = it.get("m", [it["n"].lower()])
            known.update(ms)
            if any(has(both, m) for m in ms):
                matched.append(it["n"])
    gaps = [w for w in TAX["watchlist"] if has(both, w) and w not in known]
    return dict(tags=tags, matched=matched, gaps=gaps, text=both)


def score(item, a):
    s = item.get("w", 0) + sum(a["tags"].get(t, 0) for t in item.get("t", []))
    ms = item.get("m", [item.get("n", "")]) if isinstance(item.get("n"), str) else []
    return s + (8 if any(m and has(a["text"], m) for m in ms) else 0)


def pick(role, jd=""):
    """Chọn nội dung (còn thừa để cắt dần cho vừa 1 trang)."""
    a = analyze(role, jd)
    top = lambda lst, n: sorted(lst, key=lambda x: -x[0])[:n]
    exp = top([(score(e, a), e) for e in P["experience"]], LIMITS["exp"])
    proj = top([(score(p, a), p) for p in P["projects"]], LIMITS["proj"])
    groups = []
    for g in P["skills"]:
        its = top([(score(i, a), i) for i in g["items"]], LIMITS["group_items"])
        its = [x for x in its if x[0] > 0 or len(its) <= 3]
        if its:
            groups.append([sum(s for s, _ in its), g, its])
    groups = sorted(groups, key=lambda x: -x[0])[: LIMITS["groups"]]
    return a, exp, proj, groups


def make_cv(title, a, exp, proj, groups):
    """Dựng dict CV cho build.build_html từ phần đã chọn."""
    t = esc(title.strip())
    out = {"id": "custom", "file": "Custom", "title_en": t, "title_vi": t,
           "badge_en": t.upper(), "badge_vi": t.upper()}
    best = lambda n: max([score(i, a) for g in P["skills"] for i in g["items"] if i["n"] == n] or [0])
    flat = sorted((i["n"] for _, g, its in groups for _, i in its), key=lambda n: -best(n))
    for k in ("en", "vi"):
        out["summary_" + k] = esc(tx(P["summary"], k).format(
            title=title.strip(), years=tx(P.get("years", ""), k), skills=", ".join(flat[:5])))
        out["exp_" + k] = [esc(tx(e, k)) for _, e in exp]
        out["projects_" + k] = [(esc(tx(p["n"], k)), esc(p.get("tech", "")), [esc(tx(p, k))])
                                for _, p in proj]
        out["skills_" + k] = [(esc(tx(g["g"], k)) + ":", esc(", ".join(i["n"] for _, i in its)))
                              for _, g, its in groups]
    return out


def trim(exp, proj, groups):
    """Bỏ phần điểm thấp nhất. False nếu hết gì để bỏ."""
    if len(exp) > 4:
        exp.pop()
    elif len(proj) > 2:
        proj.pop()
    elif len(exp) > 3:
        exp.pop()
    else:
        g = max((g for g in groups if len(g[2]) > 1), key=lambda g: len(g[2]), default=None)
        if not g:
            return False
        g[2].pop()
    return True


def slug(s):
    s = unicodedata.normalize("NFKD", s.replace("đ", "d").replace("Đ", "D")).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "", s.title()) or "Role"


# ------------------------------------------------------------- an toàn ------
def denylist():
    """Từ cấm riêng của hồ sơ: profiles/<id>/denylist.txt (mỗi dòng 1 từ, # = chú thích)."""
    f = os.path.join(P["_dir"], "denylist.txt")
    if not os.path.isfile(f):
        return []
    return [w.strip().lower() for w in open(f, encoding="utf-8")
            if w.strip() and not w.strip().startswith("#")]


def leaks(html_text, words):
    text = html.unescape(re.sub(r"<[^>]+>", " ", html_text)).lower()
    return [w for w in words if has(text, w)]


# --------------------------------------------------------------- sinh CV ----
def generate(role, jd="", langs=("EN", "VI"), log=print, name="", title="", avatar=""):
    """Sinh 4 file (EN/VI × Human/ATS) vào out/<id>/<Role>/. Trả về [(path, ok)]."""
    title = title.strip() or role
    name = name.strip()
    avatar = os.path.expanduser(avatar.strip())
    if not avatar and P.get("avatar"):
        avatar = os.path.join(P["_dir"], os.path.expanduser(P["avatar"]))
    if avatar and not os.path.isfile(avatar):
        raise FileNotFoundError(f"Không thấy ảnh: {avatar}")
    a, exp, proj, groups = pick(role, jd)
    d = os.path.join(OUT, P["_id"], slug(role))
    os.makedirs(d, exist_ok=True)
    img = "Avatar" + (os.path.splitext(avatar)[1].lower() if avatar else ".png")
    if avatar:
        shutil.copy(avatar, os.path.join(d, img))
    files, deny = [], denylist()
    for lang in langs:
        who = slug(name or tx(P["name"], lang.lower()))
        for kind, tag in (("human", "Human"), ("ats", "ATS")):
            e, p, g = list(exp), list(proj), [[s, gr, list(i)] for s, gr, i in groups]
            doc = None
            while True:
                base = f"CV_{who}_{slug(title)}_{lang}_{tag}"
                hp, pp = os.path.join(d, base + ".html"), os.path.join(d, base + ".pdf")
                doc = B.build_html(make_cv(title, a, e, p, g), lang.lower(), STYLE[kind],
                                   name=name or None, avatar=img if avatar else "", person=PERSON)
                with open(hp, "w", encoding="utf-8") as f:
                    f.write(doc)
                pages = B.build_pdf(hp, pp)
                if pages in ("1", "?") or not trim(e, p, g):
                    break
            bad = leaks(doc, deny)
            lost = B.missing_glyphs(doc, pp)
            ok = pages == "1" and not bad and not lost
            log(f"{'OK ' if ok else 'LỖI'} {pages} trang  {os.path.relpath(pp, ROOT)}"
                + (f"  RÒ RỈ: {', '.join(bad)}" if bad else "")
                + (f"  MẤT DẤU: {', '.join(lost[:5])}" if lost else ""))
            files.append((pp, ok))
    return files


def report(role, jd=""):
    a, exp, proj, groups = pick(role, jd)
    tags = ", ".join(f"{k}({v})" for k, v in sorted(a["tags"].items(), key=lambda x: -x[1]))
    return "\n".join([
        f"Hồ sơ      : {P['_id']}",
        f"Hướng role : {tags}",
        f"Khớp       : {', '.join(a['matched']) or '-'}",
        f"THIẾU (JD đòi, CV chưa có — không tự thêm): {', '.join(a['gaps']) or '-'}",
    ])


# ------------------------------------------------------------------ check ---
def check():
    use_profile("")
    a = analyze("DevOps Engineer", "Docker, Kubernetes, CI/CD, Prometheus, AWS")
    assert a["tags"]["devops"] > a["tags"].get("frontend", 0), a["tags"]
    assert {"kubernetes", "aws"} <= set(a["gaps"]) and "Docker" in a["matched"], a
    _, exp, _, groups = pick("Frontend React developer")
    assert groups[0][1]["g"]["en"] == "Frontend", groups[0][1]["g"]
    assert pick("zzz")[0]["tags"] == {"fullstack": 3}
    assert tx({"w": 1, "en": "a", "vi": "b"}, "vi") == "b"
    assert tx({"degree": "x"}, "en") == {"degree": "x"}
    assert slug("Vũ Hữu Đô") == "VuHuuDo" and esc("A & <b>") == "A &amp; &lt;b&gt;"
    assert leaks("<p>at ACME Corp</p>", ["acme corp"]) == ["acme corp"]
    try:
        save_profile()
        raise SystemExit("hồ sơ mẫu phải là chỉ đọc")
    except PermissionError:
        pass
    import tempfile
    global PROFILES, P, PERSON
    old, PROFILES = PROFILES, tempfile.mkdtemp()
    shutil.copytree(os.path.join(old, "_template"), os.path.join(PROFILES, "_template"))
    try:
        new_profile("t1")
        assert list_profiles() == ["t1"]
        use_profile("t1")
        open(os.path.join(P["_dir"], "denylist.txt"), "w").write("# x\nAcme Corp\n")
        assert denylist() == ["acme corp"]
    finally:
        PROFILES, P, PERSON = old, None, None
        use_profile("")
    print("check OK")


# -------------------------------------------------------------------- TUI ---
def run_tui():
    from textual import work
    from textual.app import App, ComposeResult
    from textual.containers import Horizontal, Vertical, VerticalScroll
    from textual.widgets import (Button, Checkbox, Footer, Header, Input, Label, RichLog,
                                 Select, Static, TabbedContent, TabPane, TextArea)

    ids = ["vuhuudo"] + list_profiles()

    class CVApp(App):
        TITLE = "CV Generator"
        CSS = """
        #left {width: 52%; padding: 0 1;} #right {width: 48%; padding: 0 1;}
        TextArea {height: 6;} #log {height: 1fr; border: round $accent;}
        #ana {height: 7; border: round $primary; padding: 0 1;}
        .hint {color: $text-muted;} #profile-row {height: auto;}
        """
        BINDINGS = [("ctrl+g", "gen", "Tạo CV"), ("ctrl+s", "save", "Lưu hồ sơ"),
                    ("ctrl+q", "quit", "Thoát")]

        def compose(self) -> ComposeResult:
            yield Header()
            with Vertical():
                with Horizontal(id="profile-row"):
                    yield Label("Hồ sơ: ")
                    yield Select([(i, i) for i in ids], value=ids[0], allow_blank=False, id="profile")
                    yield Input(placeholder="id hồ sơ mới", id="newid")
                    yield Button("Tạo hồ sơ", id="new")
                with TabbedContent(initial="tab-gen"):
                    with TabPane("Tạo CV", id="tab-gen"):
                        with Horizontal():
                            with VerticalScroll(id="left"):
                                yield Static("Role muốn ứng tuyển (chọn nội dung):")
                                yield Input(placeholder="vd: Backend .NET Developer", id="role")
                                yield Static("Chức danh in trên CV (trống = như role):")
                                yield Input(placeholder="vd: Senior Backend Engineer", id="title")
                                yield Static("Họ tên trên CV (trống = theo hồ sơ):")
                                yield Input(placeholder="theo hồ sơ", id="name")
                                yield Static("Ảnh đại diện — đường dẫn (trống = theo hồ sơ):")
                                yield Input(placeholder="~/Pictures/avatar.jpg", id="avatar")
                                yield Static("Job description (tuỳ chọn):")
                                yield TextArea(id="jd")
                                with Horizontal():
                                    yield Checkbox("EN", True, id="en")
                                    yield Checkbox("VI", True, id="vi")
                                yield Button("Tạo 2 loại CV  (Ctrl+G)", variant="success", id="go")
                            with VerticalScroll(id="right"):
                                yield Static("Phân tích:")
                                yield Static("Nhập role để xem phân tích.", id="ana")
                                yield Static("Kết quả:")
                                yield RichLog(id="log", wrap=True, markup=False)
                    with TabPane("Hồ sơ", id="tab-prof"):
                        with VerticalScroll():
                            yield Static("Sửa thông tin cá nhân của hồ sơ đang chọn, rồi Ctrl+S.",
                                         classes="hint")
                            for key, ph in (("pf-name-en", "Họ tên (EN)"), ("pf-name-vi", "Họ tên (VI)"),
                                            ("pf-phone", "+84 ..."), ("pf-email", "you@example.com"),
                                            ("pf-location-en", "City, Country (EN)"),
                                            ("pf-location-vi", "Thành phố (VI)"),
                                            ("pf-avatar", "đường dẫn ảnh")):
                                yield Static(ph)
                                yield Input(id=key)
                            yield Static("Từ cấm, mỗi dòng 1 từ (tên hệ thống/khách hàng nội bộ…):")
                            yield TextArea(id="pf-deny")
            yield Footer()

        # --- tiện ích
        def q(self, i):
            return self.query_one(i, Input).value.strip()

        def fill_profile_form(self):
            for key, val in (("pf-name-en", tx(P["name"], "en")), ("pf-name-vi", tx(P["name"], "vi")),
                             ("pf-phone", P.get("phone", "")), ("pf-email", P.get("email", "")),
                             ("pf-location-en", tx(P.get("location") or "", "en")),
                             ("pf-location-vi", tx(P.get("location") or "", "vi")),
                             ("pf-avatar", P.get("avatar", ""))):
                self.query_one("#" + key, Input).value = val
            self.query_one("#pf-deny", TextArea).text = "\n".join(denylist())
            ro = P.get("_readonly", False)
            for w in self.query(Input).filter(".pf-name-en, .pf-phone, .pf-email"):
                w.disabled = ro

        def vals(self):
            return self.q("#role"), self.query_one("#jd", TextArea).text

        def opts(self):
            return dict(title=self.q("#title"), name=self.q("#name"), avatar=self.q("#avatar"))

        def on_mount(self):
            use_profile(ids[0])
            self.fill_profile_form()

        def on_select_changed(self, e):
            use_profile(str(e.value))
            self.fill_profile_form()
            self.refresh_ana()
            self.query_one("#log", RichLog).write(f"Hồ sơ: {P['_id']}")

        def refresh_ana(self):
            r, j = self.vals()
            self.query_one("#ana", Static).update(report(r, j) if r else "Nhập role để xem phân tích.")

        def on_input_changed(self, e):
            if e.input.id == "role":
                self.refresh_ana()

        def on_text_area_changed(self, e):
            if e.text_area.id == "jd":
                self.refresh_ana()

        def on_button_pressed(self, e):
            if e.button.id == "go":
                self.action_gen()
            elif e.button.id == "new":
                pid = self.q("#newid")
                try:
                    path = new_profile(pid)
                except Exception as ex:  # noqa: BLE001
                    self.query_one("#log", RichLog).write(f"Lỗi: {ex}")
                    return
                self.query_one("#newid", Input).value = ""
                sel = self.query_one("#profile", Select)
                sel.set_options([(i, i) for i in ["vuhuudo"] + list_profiles()])
                sel.value = pid
                self.query_one("#log", RichLog).write(f"Đã tạo {path}")

        def action_save(self):
            log = self.query_one("#log", RichLog)
            try:
                if P.get("_readonly"):
                    raise PermissionError("Hồ sơ mẫu chỉ đọc — tạo hồ sơ mới rồi sửa bản sao.")
                P["name"] = {"en": self.q("#pf-name-en"), "vi": self.q("#pf-name-vi")}
                loc = {"en": self.q("#pf-location-en"), "vi": self.q("#pf-location-vi")}
                P["location"] = loc
                P["phone"], P["email"] = self.q("#pf-phone"), self.q("#pf-email")
                P["avatar"] = self.q("#pf-avatar")
                P["contact_line"] = {}
                for k in ("en", "vi"):
                    items = [("pin", loc[k]), ("phone", P["phone"])]
                    if P["email"]:
                        items.append(("mail", f'<a href="mailto:{P["email"]}">{P["email"]}</a>'))
                    for key, kind in (("github", "github"), ("linkedin", "linkedin")):
                        if P.get(key):
                            url = P[key] if P[key].startswith("http") else "https://" + P[key]
                            items.append((kind, f'<a href="{quote(url, safe=":/%")}">{P[key]}</a>'))
                    P["contacts"][k] = [list(i) for i in items if i[1]]
                    P["contact_line"][k] = " &bull; ".join(re.sub(r"<[^>]+>", "", c[1])
                                                           for c in P["contacts"][k])
                deny = [w.strip() for w in self.query_one("#pf-deny", TextArea).text.splitlines()
                        if w.strip() and not w.strip().startswith("#")]
                path = os.path.join(P["_dir"], "denylist.txt")
                with open(path, "w", encoding="utf-8") as f:
                    f.write("\n".join(deny) + ("\n" if deny else ""))
                global PERSON
                PERSON = _person(P)
                log.write(f"Đã lưu {save_profile()} + {len(deny)} từ cấm")
            except Exception as ex:  # noqa: BLE001
                log.write(f"Lỗi: {ex}")

        def action_gen(self):
            r, j = self.vals()
            langs = [l for l, i in (("EN", "#en"), ("VI", "#vi"))
                     if self.query_one(i, Checkbox).value]
            log = self.query_one("#log", RichLog)
            if not r or not langs:
                log.write("Cần nhập role và chọn ít nhất 1 ngôn ngữ.")
                return
            log.write(f"Đang tạo CV cho: {r} ...")
            self.render_job(r, j, langs, self.opts())

        @work(thread=True, exclusive=True)
        def render_job(self, r, j, langs, o):
            log = self.query_one("#log", RichLog)
            w = lambda m: self.call_from_thread(log.write, m)
            try:
                res = generate(r, j, langs, w, **o)
                ok = all(x for _, x in res)
                w("Xong." + ("" if ok else " CÓ LỖI — xem dòng LỖI ở trên.") +
                  f" Thư mục: out/{P['_id']}/{slug(r)}/")
            except Exception as ex:  # noqa: BLE001
                w(f"Lỗi: {ex}")

    CVApp().run()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", help="id trong profiles/ (mặc định: hồ sơ mẫu từ content/)")
    ap.add_argument("--new", metavar="ID", help="tạo hồ sơ mới từ mẫu rồi thoát")
    ap.add_argument("--list", action="store_true", help="liệt kê hồ sơ")
    ap.add_argument("--role")
    ap.add_argument("--jd", help="file chứa job description")
    ap.add_argument("--lang", default="EN,VI")
    ap.add_argument("--title", default="", help="chức danh hiển thị (mặc định = role)")
    ap.add_argument("--name", default="", help="họ tên (mặc định theo hồ sơ)")
    ap.add_argument("--avatar", default="", help="đường dẫn ảnh đại diện")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        check()
    elif a.list:
        print("vuhuudo (mẫu, chỉ đọc)")
        print("\n".join(list_profiles()) or "(chưa có hồ sơ riêng)")
    elif a.new:
        print("Đã tạo", new_profile(a.new), "— sửa file này hoặc dùng TUI rồi chạy lại.")
    elif a.role:
        use_profile(a.profile or "")
        jd = open(a.jd, encoding="utf-8").read() if a.jd else ""
        print(report(a.role, jd))
        res = generate(a.role, jd, a.lang.upper().split(","),
                       name=a.name, title=a.title, avatar=a.avatar)
        sys.exit(0 if all(ok for _, ok in res) else 1)
    else:
        use_profile(a.profile or "")
        run_tui()
