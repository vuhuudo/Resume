using System.Text.Json.Serialization;

namespace VietCv;

/// <summary>Hồ sơ một người: thông tin cá nhân + ngân hàng nội dung CV.</summary>
public sealed class Profile
{
    public Dictionary<string, string> Name { get; set; } = new() { ["en"] = "Your Name", ["vi"] = "Tên Của Bạn" };
    public string Avatar { get; set; } = "";
    public Dictionary<string, string>? Location { get; set; }
    public string Phone { get; set; } = "";
    public string Email { get; set; } = "";
    public string Github { get; set; } = "";
    public string Linkedin { get; set; } = "";
    public Dictionary<string, string> ContactLine { get; set; } = new();
    public Dictionary<string, List<string[]>> Contacts { get; set; } = new();
    public Dictionary<string, JobInfo> Job { get; set; } = new();
    public Dictionary<string, EducationInfo> Education { get; set; } = new();
    public Dictionary<string, LanguageInfo> Languages { get; set; } = new();
    public Dictionary<string, string>? Availability { get; set; }
    public Dictionary<string, string> Years { get; set; } = new() { ["en"] = "1", ["vi"] = "1" };
    public Dictionary<string, string> Summary { get; set; } = new();
    public List<Experience> Experience { get; set; } = new();
    public List<ProjectItem> Projects { get; set; } = new();
    public List<SkillGroup> Skills { get; set; } = new();
    public List<string>? Denylist { get; set; }
}

public sealed class JobInfo
{
    public string Title { get; set; } = "";
    public string Org { get; set; } = "";
    public string Meta { get; set; } = "";
}

public sealed class EducationInfo
{
    public string Strong { get; set; } = "";
    public string Line { get; set; } = "";
    public string Years { get; set; } = "";
    public string Ats { get; set; } = "";
}

public sealed class LanguageInfo
{
    public string Ats { get; set; } = "";
    public List<string[]> Items { get; set; } = new();
}

public sealed class Experience
{
    public int W { get; set; } = 1;
    public List<string> T { get; set; } = new();
    public Dictionary<string, string> Text { get; set; } = new();
    public string En { get => Text.GetValueOrDefault("en", ""); set => Text["en"] = value; }
    public string Vi { get => Text.GetValueOrDefault("vi", ""); set => Text["vi"] = value; }
}

public sealed class ProjectItem
{
    public int W { get; set; } = 1;
    public List<string> T { get; set; } = new();
    public Dictionary<string, string> N { get; set; } = new();
    public string Tech { get; set; } = "";
    public string En { get; set; } = "";
    public string Vi { get; set; } = "";
}

public sealed class SkillGroup
{
    public Dictionary<string, string> G { get; set; } = new();
    public List<Skill> Items { get; set; } = new();
}

public sealed class Skill
{
    public string N { get; set; } = "";
    public List<string>? M { get; set; }
    public List<string> T { get; set; } = new();
}

public sealed class Taxonomy
{
    public Dictionary<string, List<string>> Aliases { get; set; } = new();
    public List<string> Watchlist { get; set; } = new();
}

public sealed class RenderRequest
{
    public string? ProfileId { get; set; }
    public Profile? Profile { get; set; }
    public string Role { get; set; } = "";
    public string Title { get; set; } = "";
    public List<string> Langs { get; set; } = new() { "EN", "VI" };
}

public sealed class RenderResult
{
    public List<RenderedFile> Files { get; set; } = new();
    public List<string> Matched { get; set; } = new();
    public List<string> Gaps { get; set; } = new();
    public List<string> Warnings { get; set; } = new();
}

public sealed class RenderedFile
{
    public string Name { get; set; } = "";
    public string Url { get; set; } = "";
    public string Kind { get; set; } = "";
    public string Lang { get; set; } = "";
    public int Pages { get; set; }
}

public sealed class ImproveResult
{
    public string Text { get; set; } = "";
    public int Chars { get; set; }
    public List<Finding> Findings { get; set; } = new();
}

public sealed class Finding
{
    public string Level { get; set; } = "info";   // info | warn | risk
    public string Message { get; set; } = "";
}
