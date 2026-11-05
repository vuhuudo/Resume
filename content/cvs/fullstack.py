"""CV Full Stack Developer (.NET / React) — bản chính.

Xuất 3 bản: EN (ATS), EN (visual), VI (visual).
Nội dung mô tả chung (không nêu tên hệ thống nội bộ/số liệu đơn vị) — repo công khai.
"""
CV = {
    "id": "fullstack",
    "file": "FullStack",
    "outputs": [("en", "ats"), ("en", "visual"), ("vi", "visual")],

    "title_en": "Full Stack Developer — .NET / React",
    "title_vi": "Lập trình viên Full Stack — .NET / React",
    "badge_en": "FULL STACK DEVELOPER",
    "badge_vi": "LẬP TRÌNH VIÊN FULL STACK",

    "summary_en": (
        "Full Stack Developer with 1.5 years of experience building and operating enterprise web "
        "platforms. Delivers end-to-end across .NET (ABP Framework), React + TypeScript, SQL Server and "
        "Docker/Linux with CI/CD and monitoring. Shipped reporting, single sign-on (OpenID Connect) and "
        "data platforms to production. AI graduate."
    ),
    "summary_vi": (
        "Lập trình viên Full Stack với 1,5 năm kinh nghiệm xây dựng và vận hành nền tảng web doanh "
        "nghiệp. Làm trọn gói với .NET (ABP Framework), React + TypeScript, SQL Server và Docker/Linux "
        "kèm CI/CD, giám sát. Đã đưa nền tảng báo cáo, đăng nhập tập trung (OpenID Connect) và dữ liệu "
        "lên production. Tốt nghiệp ngành AI."
    ),

    "skills_en": [
        ("Languages:", "C#, TypeScript / JavaScript, Python, Rust, SQL, Bash"),
        ("Backend:", ".NET (ASP.NET Core), ABP Framework, Entity Framework Core, REST APIs"),
        ("Frontend:", "React, Svelte, Vite, HTML5, CSS3, responsive design"),
        ("Data &amp; Storage:", "SQL Server (T-SQL), PostgreSQL, ClickHouse, S3, Pandas / NumPy"),
        ("DevOps:", "Docker, Linux, Git, CI/CD, reverse proxy, Prometheus &amp; Grafana, "
                    "backup &amp; restore"),
        ("Auth &amp; Security:", "OpenID Connect / OAuth2, PKCE, RBAC, audit logging"),
        ("AI &amp; Testing:", "LLM API integration, Python automation · xUnit, Vitest, Playwright "
                             "(CI gates)"),
    ],
    "skills_vi": [
        ("Ngôn ngữ:", "C#, TypeScript / JavaScript, Python, Rust, SQL, Bash"),
        ("Backend:", ".NET (ASP.NET Core), ABP Framework, Entity Framework Core, REST API"),
        ("Frontend:", "React, Svelte, Vite, HTML5, CSS3, responsive design"),
        ("Dữ liệu &amp; Lưu trữ:", "SQL Server (T-SQL), PostgreSQL, ClickHouse, S3, Pandas / NumPy"),
        ("DevOps:", "Docker, Linux, Git, CI/CD, reverse proxy, Prometheus &amp; Grafana, "
                    "backup &amp; restore"),
        ("Xác thực &amp; Bảo mật:", "OpenID Connect / OAuth2, PKCE, RBAC, nhật ký kiểm toán"),
        ("AI &amp; Kiểm thử:", "Tích hợp LLM API, tự động hóa Python · xUnit, Vitest, Playwright "
                               "(cổng CI)"),
    ],

    "exp_en": [
        "<b>Full-stack:</b> Built platforms end-to-end — .NET (ABP) APIs, React + TypeScript UIs and "
        "SQL Server — including an enterprise reporting platform and a project-data platform, both in "
        "production.",
        "<b>Identity &amp; SSO:</b> Implemented central single sign-on with <b>OpenID Connect / "
        "OAuth2</b>: PKCE flows, service-to-service access, role-based permissions, session management "
        "and audit logging.",
        "<b>Data platform:</b> Built a Medallion <b>data lakehouse</b> (ClickHouse, PostgreSQL, S3) with "
        "a Python API, Svelte UI and a <b>Rust</b> core for file parsing &amp; export; sharded CI cut "
        "test time by ~65%.",
        "<b>DevOps:</b> Operated dev / UAT / production on Docker &amp; Linux: CI/CD with test gates, "
        "monitoring, alerting, backups and rollback-safe releases.",
        "<b>AI &amp; automation:</b> Python and LLM-API workflows that remove repetitive manual "
        "processing for management teams.",
        "<b>Ownership:</b> Coordinated an internal platform rollout across branch offices and reported "
        "progress to management.",
    ],
    "exp_vi": [
        "<b>Full Stack:</b> Xây dựng nền tảng trọn gói — API .NET (ABP), giao diện React + TypeScript, "
        "SQL Server — gồm nền tảng báo cáo doanh nghiệp và nền tảng dữ liệu dự án, đều đã lên "
        "production.",
        "<b>Định danh &amp; SSO:</b> Triển khai đăng nhập tập trung <b>OpenID Connect / OAuth2</b>: "
        "luồng PKCE, truy cập giữa các dịch vụ, phân quyền theo vai trò, quản lý phiên và nhật ký "
        "kiểm toán.",
        "<b>Nền tảng dữ liệu:</b> Xây dựng <b>data lakehouse</b> kiểu Medallion (ClickHouse, PostgreSQL, "
        "S3) với API Python, giao diện Svelte và lõi <b>Rust</b> xử lý/xuất tệp; CI chia shard giảm "
        "~65% thời gian test.",
        "<b>DevOps:</b> Vận hành dev / UAT / production trên Docker &amp; Linux: CI/CD có cổng kiểm "
        "thử, giám sát, cảnh báo, backup và phát hành có rollback.",
        "<b>AI &amp; tự động hóa:</b> Quy trình Python và LLM API giúp loại bỏ xử lý thủ công lặp lại "
        "cho bộ phận quản lý.",
        "<b>Trách nhiệm:</b> Điều phối triển khai nền tảng nội bộ tại các chi nhánh và báo cáo tiến độ "
        "lên quản lý.",
    ],

    "projects_en": [
        ("Enterprise reporting platform",
         "ABP / .NET · React · TypeScript · SQL Server · Docker",
         ["Period reporting for <b>dozens of entities</b>: data import &amp; validation, approval "
          "workflow, dashboards.",
          "Three-environment delivery with automated tests, health checks and backup/restore "
          "procedures."]),
        ("Central authentication (SSO) service",
         "ABP / .NET · OpenID Connect · OAuth2 · SQL Server",
         ["Single sign-on, RBAC, session and audit management for internal applications.",
          "Service-to-service APIs (user lookup, application members) used by other systems."]),
        ("Data lakehouse &amp; analytics",
         "Python · Rust · ClickHouse · PostgreSQL · Svelte",
         ["Medallion-style pipeline with REST APIs, dashboards and automated tests."]),
    ],
    "projects_vi": [
        ("Nền tảng báo cáo doanh nghiệp",
         "ABP / .NET · React · TypeScript · SQL Server · Docker",
         ["Báo cáo theo kỳ cho <b>hàng chục đơn vị</b>: nhập &amp; kiểm tra dữ liệu, quy trình duyệt, "
          "dashboard.",
          "Vận hành 3 môi trường với kiểm thử tự động, health check và backup/restore."]),
        ("Dịch vụ xác thực tập trung (SSO)",
         "ABP / .NET · OpenID Connect · OAuth2 · SQL Server",
         ["Đăng nhập một lần, RBAC, quản lý phiên và nhật ký kiểm toán cho các ứng dụng nội bộ.",
          "API service-to-service (tra cứu người dùng, thành viên ứng dụng) cho các hệ thống khác."]),
        ("Data lakehouse &amp; phân tích",
         "Python · Rust · ClickHouse · PostgreSQL · Svelte",
         ["Pipeline kiểu Medallion với REST API, dashboard và kiểm thử tự động."]),
    ],

    "soft_skills_en": [
        "Self-learning &amp; adaptable",
        "Teamwork &amp; collaboration",
        "Technical problem-solving",
        "Clear written communication",
    ],
    "soft_skills_vi": [
        "Tự học &amp; thích nghi nhanh",
        "Làm việc nhóm",
        "Giải quyết vấn đề kỹ thuật",
        "Viết tài liệu rõ ràng",
    ],
}
