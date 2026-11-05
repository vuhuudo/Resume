using System.Text.Json;
using System.Text.RegularExpressions;

namespace VietCv;

/// <summary>Nội dung một bản CV sau khi chọn lọc, theo từng ngôn ngữ.</summary>
public sealed class CvDoc
{
    public string Role { get; set; } = "";
    public Dictionary<string, string> Title { get; } = new();
    public Dictionary<string, string> Badge { get; } = new();
    public Dictionary<string, string> Summary { get; } = new();
    public Dictionary<string, List<string>> Exp { get; } = new();
    public Dictionary<string, List<(string Name, string Tech, string Desc)>> Projects { get; } = new();
    public Dictionary<string, List<(string K, string V)>> Skills { get; } = new();
}

public static partial class Renderer
{
    private static readonly JsonElement Design = JsonSerializer.Deserialize<JsonElement>(
        File.ReadAllText(Path.Combine(AppContext.BaseDirectory, "Cv", "design.json")));

    private static string Tpl(string style) =>
        File.ReadAllText(Path.Combine(AppContext.BaseDirectory, "templates", style == "ats" ? "ats.html" : "visual.html"));

    private static string Icon(string kind) =>
        Design.GetProperty("icons").TryGetProperty(kind, out var v) ? v.GetString() ?? "" : "";

    private static string Label(string lang, string key) =>
        Design.GetProperty("labels").GetProperty(lang).GetProperty(key).GetString() ?? key;

    public static CvDoc BuildDoc(Profile p, Taxonomy tax, string role, string jd, int limitExp = 7, int limitProj = 3)
    {
        var (tags, _, _) = CvLogic.Analyze(p, tax, role, jd);
        var both = role.ToLowerInvariant() + "\n" + jd.ToLowerInvariant();
        var doc = new CvDoc { Role = role };
        var title = CvLogic.Esc(role.Trim());
        foreach (var lang in new[] { "en", "vi" })
        {
            doc.Title[lang] = title;
            doc.Badge[lang] = role.Trim().ToUpperInvariant();
        }
        var (exp, proj, groups) = CvLogic.Pick(p, tax, role, jd, limitExp, limitProj);
        var flat = groups.SelectMany(g => g.Items)
            .OrderByDescending(i => i.T.Sum(t => tags.GetValueOrDefault(t)) + (i.M ?? new()).Count(m => CvLogic.Has(both, m)) * 8)
            .Select(i => i.N).ToList();
        foreach (var lang in new[] { "en", "vi" })
        {
            doc.Summary[lang] = CvLogic.Esc((CvLogic.Tx(p.Summary, lang))
                .Replace("{title}", role.Trim())
                .Replace("{years}", CvLogic.Tx(p.Years, lang))
                .Replace("{skills}", string.Join(", ", flat.Take(5))));
            doc.Exp[lang] = exp.Select(e => CvLogic.Esc(CvLogic.Tx(e.Text, lang))).ToList();
            doc.Projects[lang] = proj.Select(x => (
                CvLogic.Esc(CvLogic.Tx(x.N, lang)),
                CvLogic.Esc(x.Tech),
                CvLogic.Esc(lang == "en" ? x.En : x.Vi))).ToList();
            doc.Skills[lang] = groups.Select(g => (
                CvLogic.Esc(CvLogic.Tx(g.G.G, lang)) + ":",
                CvLogic.Esc(string.Join(", ", g.Items.Select(i => i.N))))).ToList();
        }
        return doc;
    }

    public static string Html(Profile p, CvDoc doc, string lang, string style, string? name, string avatar)
    {
        var n = string.IsNullOrWhiteSpace(name) ? CvLogic.Tx(p.Name, lang) : name;
        var job = p.Job.GetValueOrDefault(lang) ?? p.Job.GetValueOrDefault("en") ?? new JobInfo();
        var edu = p.Education.GetValueOrDefault(lang) ?? p.Education.GetValueOrDefault("en") ?? new EducationInfo();
        var lng = p.Languages.GetValueOrDefault(lang) ?? p.Languages.GetValueOrDefault("en") ?? new LanguageInfo();
        var contacts = (p.Contacts.GetValueOrDefault(lang) ?? new List<string[]>())
            .Where(c => c.Length > 1 && c[1].Length > 0);
        var bullets = string.Join("\n", doc.Exp[lang].Select(b => $"      <li>{b}</li>"));
        var projects = string.Join("\n", doc.Projects[lang].Select(x => style == "ats"
            ? $"  <div class=\"proj\">\n    <p class=\"name\">{x.Name}</p>\n    <p class=\"tech\">{x.Tech}</p>\n    <ul>\n      <li>{x.Desc}</li>\n    </ul>\n  </div>"
            : $"      <div class=\"project-block\">\n        <div class=\"project-title\">{x.Name}</div>\n        <div class=\"project-tech\">{x.Tech}</div>\n        <ul class=\"bullet-list\">\n          <li>{x.Desc}</li>\n        </ul>\n      </div>"));
        var skills = string.Join("\n", doc.Skills[lang].Select(s => style == "ats"
            ? $"    <p><b>{s.K}</b> {s.V}</p>"
            : $"        <div class=\"skill-row\"><div class=\"skill-category\">{s.K}</div><div class=\"skill-details\">{s.V}</div></div>"));
        var contactItems = string.Join("\n", contacts.Select(c => $"        <li>{Icon(c[0])}<span>{c[1]}</span></li>"));
        var langItems = string.Join("\n", lng.Items.Where(i => i.Length > 1)
            .Select(i => $"        <li><strong>{System.Net.WebUtility.HtmlEncode(i[0])}:</strong> {System.Net.WebUtility.HtmlEncode(i[1])}</li>"));

        var map = new Dictionary<string, string>
        {
            ["{{HTML_LANG}}"] = lang,
            ["{{DOC_TITLE}}"] = $"{n} — {doc.Title[lang]} — CV",
            ["{{NAME}}"] = System.Net.WebUtility.HtmlEncode(n),
            ["{{TITLE}}"] = doc.Title[lang],
            ["{{AVATAR}}"] = avatar,
            ["{{BADGE}}"] = doc.Badge[lang],
            ["{{CONTACT}}"] = CvLogic.Tx(p.ContactLine, lang),
            ["{{AVAILABILITY}}"] = p.Availability is { Count: > 0 } av && av.TryGetValue(lang, out var avail) ? avail : "",
            ["{{CONTACTS}}"] = contactItems,
            ["{{L_CONTACT}}"] = Label(lang, "contact"),
            ["{{L_SUMMARY}}"] = Label(lang, "summary"),
            ["{{SUMMARY}}"] = doc.Summary[lang],
            ["{{L_SKILLS}}"] = Label(lang, style == "ats" ? "skills_ats" : "skills"),
            ["{{SKILLS}}"] = skills,
            ["{{L_EXPERIENCE}}"] = Label(lang, "experience"),
            ["{{JOB_TITLE}}"] = job.Title,
            ["{{JOB_ORG}}"] = job.Org,
            ["{{JOB_META}}"] = job.Meta,
            ["{{BULLETS}}"] = bullets,
            ["{{L_PROJECTS}}"] = Label(lang, "projects"),
            ["{{PROJECTS}}"] = projects,
            ["{{L_EDU_LANG}}"] = Label(lang, "education_languages"),
            ["{{EDUCATION_LINE}}"] = $"{edu.Ats} &nbsp;·&nbsp; {lng.Ats}",
            ["{{L_EDUCATION}}"] = Label(lang, "education"),
            ["{{EDU_STRONG}}"] = edu.Strong,
            ["{{EDU_LINE}}"] = edu.Line,
            ["{{EDU_YEARS}}"] = edu.Years,
            ["{{L_LANGUAGES}}"] = Label(lang, "languages"),
            ["{{LANGUAGES}}"] = langItems,
            ["{{SOFT_SKILLS_SECTION}}"] = "",
        };
        var html = Tpl(style);
        foreach (var (k, v) in map) html = html.Replace(k, v ?? "");
        if (style != "ats" && string.IsNullOrWhiteSpace(avatar))
            html = Regex.Replace(html, "<div class=\"profile-img-container\">.*?</div>", "", RegexOptions.Singleline);
        return html;
    }
}
