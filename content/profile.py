"""Thông tin chung cho mọi bản CV: tên, liên hệ, công việc, học vấn, ngôn ngữ, nhãn mục."""

NAME = {"en": "Vu Huu Do", "vi": "Vũ Hữu Đô"}

# --- Liên hệ -----------------------------------------------------------------
CONTACT_LINE = {
    "en": (
        "Ho Chi Minh City, Vietnam &bull; +84 347 299 934 &bull; vuhuudo2004@gmail.com "
        "&bull; github.com/vuhuudo &bull; linkedin.com/in/vũ-hữu-đô-b899bb360"
    ),
    "vi": (
        "TP. Hồ Chí Minh, Việt Nam &bull; +84 347 299 934 &bull; vuhuudo2004@gmail.com "
        "&bull; github.com/vuhuudo &bull; linkedin.com/in/vũ-hữu-đô-b899bb360"
    ),
}

# --- Sẵn sàng nhận việc ------------------------------------------------------
AVAILABILITY = {
    "en": "Available from mid-November 2026",
    "vi": "Có thể nhận việc từ giữa tháng 11/2026",
}

_ICONS = {
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    "github": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>',
}

# (icon, nội dung HTML) — dùng cho sidebar bản "visual"
CONTACT_ITEMS = {
    "en": [
        ("pin", "Ho Chi Minh City, Vietnam"),
        ("phone", "+84 347 299 934"),
        ("mail", '<a href="mailto:vuhuudo2004@gmail.com">vuhuudo2004@gmail.com</a>'),
        ("github", '<a href="https://github.com/vuhuudo">github.com/vuhuudo</a>'),
        ("linkedin", '<a href="https://www.linkedin.com/in/v%C5%A9-h%E1%BB%AFu-%C4%91%C3%B4-b899bb360/">linkedin.com/in/vũ-hữu-đô-b899bb360</a>'),
    ],
    "vi": [
        ("pin", "TP. Hồ Chí Minh, Việt Nam"),
        ("phone", "+84 347 299 934"),
        ("mail", '<a href="mailto:vuhuudo2004@gmail.com">vuhuudo2004@gmail.com</a>'),
        ("github", '<a href="https://github.com/vuhuudo">github.com/vuhuudo</a>'),
        ("linkedin", '<a href="https://www.linkedin.com/in/v%C5%A9-h%E1%BB%AFu-%C4%91%C3%B4-b899bb360/">linkedin.com/in/vũ-hữu-đô-b899bb360</a>'),
    ],
}

# --- Công việc ---------------------------------------------------------------
JOB = {
    "en": {
        "title": "Web &amp; Database Developer",
        "org": "Hoan Cau Group",
        "meta": "June 2025 – November 2026 · 1 yr 5 mos · Ho Chi Minh City, Vietnam",
    },
    "vi": {
        "title": "Lập trình viên Web &amp; Cơ sở dữ liệu",
        "org": "Tập đoàn Hoàn Cầu",
        "meta": "06/2025 - 11/2026 (1 năm 5 tháng) · TP. Hồ Chí Minh",
    },
}

# --- Học vấn -----------------------------------------------------------------
EDUCATION = {
    "en": {
        "strong": "Bachelor of Artificial Intelligence",
        "line": "Van Lang University",
        "years": "2023 - 2026",
        "ats": "Bachelor of Artificial Intelligence — Van Lang University, Ho Chi Minh City (2023 – 2026)",
    },
    "vi": {
        "strong": "Cử nhân Trí tuệ nhân tạo",
        "line": "Đại học Văn Lang",
        "years": "2023 - 2026",
        "ats": "Cử nhân Trí tuệ nhân tạo — Đại học Văn Lang (2023 - 2026)",
    },
}

# --- Ngôn ngữ ----------------------------------------------------------------
LANGUAGES = {
    "en": {"ats": "Vietnamese (native) · English (elementary)",
           "items": [("Vietnamese", "Native"), ("English", "Elementary")]},
    "vi": {"ats": "Tiếng Việt (bản ngữ) · Tiếng Anh (cơ bản)",
           "items": [("Tiếng Việt", "Bản ngữ"), ("Tiếng Anh", "Cơ bản")]},
}

# --- Nhãn mục (section headings) --------------------------------------------
LABELS = {
    "en": {
        "contact": "Contact",
        "summary": "Summary",
        "education": "Education",
        "languages": "Languages",
        "soft_skills": "Soft Skills",
        "experience": "Professional Experience",
        "projects": "Selected Projects",
        "skills": "Technical Skills",
        "skills_ats": "Core Skills",
        "education_languages": "Education &amp; Languages",
    },
    "vi": {
        "contact": "Liên hệ",
        "summary": "Tóm tắt",
        "education": "Học vấn",
        "languages": "Ngôn ngữ",
        "soft_skills": "Kỹ năng mềm",
        "experience": "Kinh nghiệm làm việc",
        "projects": "Dự án tiêu biểu",
        "skills": "Kỹ năng chuyên môn",
        "skills_ats": "Kỹ năng chính",
        "education_languages": "Học vấn &amp; Ngôn ngữ",
    },
}


def icon(name: str) -> str:
    return _ICONS[name]
