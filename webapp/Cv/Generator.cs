namespace VietCv;

public static class Generator
{
    /// <summary>Sinh CV: mỗi ngôn ngữ × (Human, ATS), tự cắt cho vừa 1 trang, kiểm tra từ cấm + font.</summary>
    public static RenderResult Render(Store store, string id, Profile p, string role, string title, List<string> langs)
    {
        var res = new RenderResult();
        p = CvLogic.AutoTag(p, store.Taxonomy);
        var dir = store.DirFor(id, role);
        var display = string.IsNullOrWhiteSpace(title) ? role.Trim() : title.Trim();
        var doc = Renderer.BuildDoc(p, store.Taxonomy, display, "");

        var avatar = "";
        if (!string.IsNullOrWhiteSpace(p.Avatar) && File.Exists(p.Avatar))
        {
            avatar = "Avatar" + Path.GetExtension(p.Avatar).ToLowerInvariant();
            File.Copy(p.Avatar, Path.Combine(dir, avatar), true);
        }

        // Font nhúng sẵn (không phụ thuộc font hệ thống — giữ đúng dấu tiếng Việt)
        var fontsSrc = Path.Combine(AppContext.BaseDirectory, "assets", "fonts");
        if (Directory.Exists(fontsSrc))
        {
            var fontsDst = Path.Combine(dir, "fonts");
            Directory.CreateDirectory(fontsDst);
            foreach (var f in Directory.GetFiles(fontsSrc))
                File.Copy(f, Path.Combine(fontsDst, Path.GetFileName(f)), true);
        }

        foreach (var raw in langs)
        {
            var lang = raw.ToLowerInvariant();
            if (lang is not ("en" or "vi")) continue;

            var (exp, proj, groups) = CvLogic.Pick(p, store.Taxonomy, role, "");

            string BuildHtml(string style)
            {
                var work = doc.Clone();
                work.Exp[lang] = exp.Select(e => CvLogic.Esc(CvLogic.Tx(e.Text, lang))).ToList();
                work.Projects[lang] = proj.Select(x => (
                    CvLogic.Esc(CvLogic.Tx(x.N, lang)), CvLogic.Esc(x.Tech),
                    CvLogic.Esc(lang == "en" ? x.En : x.Vi))).ToList();
                work.Skills[lang] = groups.Select(g => (
                    CvLogic.Esc(CvLogic.Tx(g.G.G, lang)) + ":",
                    CvLogic.Esc(string.Join(", ", g.Items.Select(i => i.N))))).ToList();
                return Renderer.Html(p, work, lang, style, null, avatar);
            }

            foreach (var (kind, tag) in new[] { ("human", "Human"), ("ats", "ATS") })
            {
                var style = kind == "ats" ? "ats" : "visual";
                var baseName = $"CV_{CvLogic.Slug(CvLogic.Tx(p.Name, lang))}_{CvLogic.Slug(display)}_{lang.ToUpperInvariant()}_{tag}";
                var htmlPath = Path.Combine(dir, baseName + ".html");
                var pdfPath = Path.Combine(dir, baseName + ".pdf");

                var html = BuildHtml(style);
                File.WriteAllText(htmlPath, html);
                var pages = Pdf.Print(htmlPath, pdfPath);
                while (pages > 1 && CvLogic.Trim(exp, proj, groups))
                {
                    html = BuildHtml(style);
                    File.WriteAllText(htmlPath, html);
                    pages = Pdf.Print(htmlPath, pdfPath);
                }

                var leaks = CvLogic.Leaks(html, p.Denylist ?? new());
                var lost = CvLogic.MissingGlyphs(html, pdfPath);
                if (pages > 1) res.Warnings.Add($"{baseName}: {pages} trang — chưa cắt đủ để vừa 1 trang.");
                if (leaks.Count > 0) res.Warnings.Add($"{baseName}: RÒ RỈ từ cấm → {string.Join(", ", leaks)}");
                if (lost.Count > 0) res.Warnings.Add($"{baseName}: mất dấu tiếng Việt → {string.Join(", ", lost.Take(5))}");
                res.Files.Add(new RenderedFile
                {
                    Name = baseName + ".pdf",
                    Url = $"/files/{id}/{Uri.EscapeDataString(CvLogic.Slug(role))}/{baseName}.pdf",
                    Kind = kind,
                    Lang = lang,
                    Pages = pages,
                });
            }
        }
        var (_, matched, gaps) = CvLogic.Analyze(p, store.Taxonomy, role, "");
        res.Matched = matched;
        res.Gaps = gaps;
        return res;
    }
}

public static class CvDocExt
{
    public static CvDoc Clone(this CvDoc doc)
    {
        var c = new CvDoc { Role = doc.Role };
        foreach (var lang in new[] { "en", "vi" })
        {
            c.Title[lang] = doc.Title[lang];
            c.Badge[lang] = doc.Badge[lang];
            c.Summary[lang] = doc.Summary[lang];
            c.Exp[lang] = new List<string>(doc.Exp[lang]);
            c.Projects[lang] = new List<(string, string, string)>(doc.Projects[lang]);
            c.Skills[lang] = new List<(string, string)>(doc.Skills[lang]);
        }
        return c;
    }
}
