"""CV Software Engineer (tổng quát — full stack & platform)."""
CV = {
    "id": "software-engineer",
    "file": "SoftwareEngineer",
    "outputs": [("en", "ats"), ("vi", "visual")],

    "title_en": "Software Engineer — Full Stack &amp; Platform",
    "title_vi": "Kỹ sư phần mềm — Full Stack &amp; Nền tảng",
    "badge_en": "SOFTWARE ENGINEER",
    "badge_vi": "KỸ SƯ PHẦN MỀM",

    "summary_en": (
        "Software Engineer with 1.5 years of experience building and operating enterprise web platforms. "
        "Full-stack across C#/.NET (ABP Framework), React + TypeScript, SQL Server and Docker/Linux with "
        "CI/CD. Delivered reporting, authentication (OpenID Connect) and data platforms to production. AI "
        "graduate; automates workflows with Python."
    ),
    "summary_vi": (
        "Kỹ sư phần mềm với 1,5 năm kinh nghiệm xây dựng và vận hành nền tảng web doanh nghiệp. "
        "Full-stack với C#/.NET (ABP Framework), React + TypeScript, SQL Server và Docker/Linux kèm "
        "CI/CD. Đã đưa nền tảng báo cáo, xác thực (OpenID Connect) và dữ liệu lên production. Tốt nghiệp "
        "AI; tự động hóa quy trình bằng Python."
    ),

    "skills_en": [
        ("Languages:", "C#, TypeScript / JavaScript, Python, Rust, SQL, Bash"),
        ("Backend &amp; Frontend:", ".NET (ASP.NET Core), ABP Framework, Entity Framework Core, "
                                   "REST APIs, React, Svelte, Vite"),
        ("Data &amp; Storage:", "SQL Server (T-SQL), PostgreSQL, ClickHouse, S3, Pandas / NumPy"),
        ("DevOps:", "Docker, Linux, Git, CI/CD, reverse proxy, Prometheus &amp; Grafana, "
                    "backup &amp; restore"),
        ("Auth &amp; Security:", "OpenID Connect / OAuth2, PKCE, RBAC, audit logging"),
        ("AI &amp; Testing:", "LLM API integration, Python automation · xUnit, Vitest, Playwright "
                             "(CI gates)"),
    ],
    "skills_vi": [
        ("Ngôn ngữ:", "C#, TypeScript / JavaScript, Python, Rust, SQL, Bash"),
        ("Backend &amp; Frontend:", ".NET (ASP.NET Core), ABP Framework, Entity Framework Core, "
                                   "REST API, React, Svelte, Vite"),
        ("Dữ liệu &amp; Lưu trữ:", "SQL Server (T-SQL), PostgreSQL, ClickHouse, S3, Pandas / NumPy"),
        ("DevOps:", "Docker, Linux, Git, CI/CD, reverse proxy, Prometheus &amp; Grafana, "
                    "backup &amp; restore"),
        ("Xác thực &amp; Bảo mật:", "OpenID Connect / OAuth2, PKCE, RBAC, nhật ký kiểm toán"),
        ("AI &amp; Kiểm thử:", "Tích hợp LLM API, tự động hóa Python · xUnit, Vitest, Playwright "
                               "(cổng CI)"),
    ],

    "exp_en": [
        (
            "Built internal platforms end-to-end: .NET (ABP) APIs, React + TypeScript UIs and SQL Server, "
            "including an enterprise reporting platform and a project-data platform, both in production."
        ),
        (
            "Implemented central single sign-on (OpenID Connect / OAuth2): PKCE flows, service-to-service "
            "access, role-based permissions, session management and audit logging."
        ),
        (
            "Built a data lakehouse (ClickHouse, PostgreSQL, S3) with a Python API, Svelte UI and a Rust "
            "core for file parsing and export; sharded CI cut test time by ~65%."
        ),
        (
            "Operated dev / UAT / production on Docker &amp; Linux: CI/CD with test gates, monitoring, "
            "alerting, backups and rollback-safe releases."
        ),
        (
            "Coordinated an internal platform rollout across branch offices and reported progress to "
            "management."
        ),
    ],
    "exp_vi": [
        (
            "Xây dựng nền tảng nội bộ trọn gói: API .NET (ABP), giao diện React + TypeScript, SQL Server, "
            "gồm nền tảng báo cáo doanh nghiệp và nền tảng dữ liệu dự án, đều đã lên production."
        ),
        (
            "Triển khai đăng nhập tập trung (OpenID Connect / OAuth2): luồng PKCE, truy cập giữa các dịch "
            "vụ, phân quyền theo vai trò, quản lý phiên và nhật ký kiểm toán."
        ),
        (
            "Xây dựng data lakehouse (ClickHouse, PostgreSQL, S3) với API Python, giao diện Svelte và lõi "
            "Rust xử lý/xuất tệp; CI chia shard giảm ~65% thời gian test."
        ),
        (
            "Vận hành dev / UAT / production trên Docker &amp; Linux: CI/CD có cổng kiểm thử, giám sát, "
            "cảnh báo, backup và phát hành có rollback."
        ),
        (
            "Điều phối triển khai nền tảng nội bộ tại các chi nhánh và báo cáo tiến độ lên quản lý."
        ),
    ],

    "projects_en": [
        (
            "Enterprise reporting platform",
            "ABP / .NET · React · TypeScript · SQL Server · Docker",
            [
            (
                "Period reporting for <b>dozens of entities</b>: data import &amp; validation, "
                "approval workflow, dashboards."
            ),
            (
                "Three-environment delivery with automated tests, health checks and backup/restore "
                "procedures."
            ),
            ],
        ),
        (
            "Central authentication (SSO) service",
            "ABP / .NET · OpenID Connect · OAuth2 · SQL Server",
            [
            "Single sign-on, RBAC, session and audit management for internal applications.",
            "Service-to-service APIs (user lookup, application members) used by other systems.",
            ],
        ),
        (
            "Data lakehouse &amp; analytics",
            "Python · Rust · ClickHouse · PostgreSQL · Svelte",
            [
            "Medallion-style pipeline with REST APIs, dashboards and automated tests.",
            ],
        ),
    ],
    "projects_vi": [
        (
            "Nền tảng báo cáo doanh nghiệp",
            "ABP / .NET · React · TypeScript · SQL Server · Docker",
            [
            "Báo cáo theo kỳ cho <b>hàng chục đơn vị</b>: nhập &amp; kiểm tra dữ liệu, quy trình duyệt, "
            "dashboard.",
            "Vận hành 3 môi trường với kiểm thử tự động, health check và backup/restore.",
            ],
        ),
        (
            "Dịch vụ xác thực tập trung (SSO)",
            "ABP / .NET · OpenID Connect · OAuth2 · SQL Server",
            [
            "Đăng nhập một lần, RBAC, quản lý phiên và nhật ký kiểm toán cho các ứng dụng nội bộ.",
            "API service-to-service (tra cứu người dùng, thành viên ứng dụng) cho các hệ thống khác.",
            ],
        ),
        (
            "Data lakehouse &amp; phân tích",
            "Python · Rust · ClickHouse · PostgreSQL · Svelte",
            [
            "Pipeline kiểu Medallion với REST API, dashboard và kiểm thử tự động.",
            ],
        ),
    ],
}
