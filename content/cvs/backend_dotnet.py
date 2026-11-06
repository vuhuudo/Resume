"""CV Backend Developer (.NET / C#)."""
CV = {
    "id": "backend-dotnet",
    "file": "BackendDotNet",
    "outputs": [("en", "ats"), ("en", "visual"), ("vi", "visual")],

    "title_en": "Backend Developer — .NET / C#",
    "title_vi": "Lập trình viên Backend — .NET / C#",
    "badge_en": "BACKEND DEVELOPER",
    "badge_vi": "LẬP TRÌNH VIÊN BACKEND",

    "summary_en": (
        "Backend developer with 1.5 years building .NET services. Designs APIs with ABP Framework / "
        "ASP.NET Core, EF Core and SQL Server, including data import &amp; validation pipelines and "
        "approval workflows. Strong in authentication &amp; authorization (OpenID Connect, OAuth2, RBAC) "
        "and system integrations."
    ),
    "summary_vi": (
        "Lập trình viên backend với 1,5 năm xây dựng dịch vụ .NET. Thiết kế API với ABP Framework / "
        "ASP.NET Core, EF Core và SQL Server, gồm pipeline nhập &amp; kiểm tra dữ liệu và quy trình "
        "duyệt. Mạnh về xác thực &amp; phân quyền (OpenID Connect, OAuth2, RBAC) và tích hợp hệ thống."
    ),

    "skills_en": [
        ("Backend:", "C#, .NET (ASP.NET Core), ABP Framework, Entity Framework Core, REST APIs"),
        ("Auth &amp; Security:", "OpenID Connect / OAuth2, PKCE, client credentials, RBAC, audit logging"),
        ("Data:", "SQL Server (T-SQL, migrations), PostgreSQL, ClickHouse, data pipelines &amp; validation"),
        ("Integration:", "Service-to-service APIs, data synchronisation, webhooks"),
        ("DevOps &amp; Quality:", "xUnit, CI test gates, Docker, Linux, monitoring"),
        ("Secondary:", "React + TypeScript, Python, Rust"),
    ],
    "skills_vi": [
        ("Backend:", "C#, .NET (ASP.NET Core), ABP Framework, Entity Framework Core, REST API"),
        ("Xác thực &amp; Bảo mật:", "OpenID Connect / OAuth2, PKCE, client credentials, RBAC, nhật ký kiểm toán"),
        ("Dữ liệu:", "SQL Server (T-SQL, migration), PostgreSQL, ClickHouse, pipeline &amp; kiểm tra dữ liệu"),
        ("Tích hợp:", "API service-to-service, đồng bộ dữ liệu, webhook"),
        ("DevOps &amp; Chất lượng:", "xUnit, cổng kiểm thử CI, Docker, Linux, giám sát"),
        ("Bổ trợ:", "React + TypeScript, Python, Rust"),
    ],

    "exp_en": [
        (
            "Designed and shipped .NET APIs for production platforms: enterprise reporting (import &amp; "
            "validation, approval workflows) and project data management."
        ),
        (
            "Built domain, data and API layers: ABP modules, EF Core + SQL Server schemas and migrations, "
            "REST endpoints for SPAs and other systems."
        ),
        (
            "Implemented central authentication: OpenID Connect / OAuth2, PKCE, client credentials, "
            "role-based access, session and audit tracking."
        ),
        (
            "Delivered service-to-service integrations and a data lakehouse backend (Python, ClickHouse, "
            "Rust parsing core); wired xUnit and integration tests into CI."
        ),
    ],
    "exp_vi": [
        (
            "Thiết kế và phát triển API .NET cho các nền tảng production: báo cáo doanh nghiệp (nhập "
            "&amp; kiểm tra dữ liệu, quy trình duyệt) và quản lý dữ liệu dự án."
        ),
        (
            "Xây dựng tầng domain, dữ liệu và API: module ABP, schema &amp; migration EF Core + SQL "
            "Server, REST endpoint cho SPA và hệ thống khác."
        ),
        (
            "Triển khai xác thực tập trung: OpenID Connect / OAuth2, PKCE, client credentials, phân quyền "
            "theo vai trò, theo dõi phiên và kiểm toán."
        ),
        (
            "Xây dựng tích hợp service-to-service và backend data lakehouse (Python, ClickHouse, lõi "
            "Rust); đưa test xUnit và integration test vào CI."
        ),
    ],

    "projects_en": [
        (
            "Enterprise reporting platform",
            "ABP / .NET · EF Core · SQL Server",
            [
            "Import &amp; validation pipeline, approval workflows and reporting APIs.",
            ],
        ),
        (
            "Central authentication (SSO) service",
            "ABP / .NET · OpenID Connect · SQL Server",
            [
            "OIDC flows, RBAC, session &amp; audit tracking, user-lookup APIs for other systems.",
            ],
        ),
        (
            "Project data platform",
            "ABP / .NET · EF Core · SQL Server · Docker",
            [
            "APIs for coordination, member invitations and master-data sync.",
            ],
        ),
    ],
    "projects_vi": [
        (
            "Nền tảng báo cáo doanh nghiệp",
            "ABP / .NET · EF Core · SQL Server",
            [
            "Pipeline nhập &amp; kiểm tra dữ liệu, quy trình duyệt và API báo cáo.",
            ],
        ),
        (
            "Dịch vụ xác thực tập trung (SSO)",
            "ABP / .NET · OpenID Connect · SQL Server",
            [
            (
                "Luồng OIDC, RBAC, theo dõi phiên &amp; kiểm toán, API tra cứu người dùng cho hệ thống "
                "khác."
            ),
            ],
        ),
        (
            "Nền tảng dữ liệu dự án",
            "ABP / .NET · EF Core · SQL Server · Docker",
            [
            "API điều phối, mời thành viên và đồng bộ dữ liệu danh mục.",
            ],
        ),
    ],
}
