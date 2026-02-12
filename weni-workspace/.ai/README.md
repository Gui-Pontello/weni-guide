# AI-Specific Contexts

This folder contains context files optimized for different AI tools and assistants.

## 📁 Files

- **context.md** - General AI context (comprehensive)
- **cursor-rules.md** - Rules for Cursor AI
- **claude-context.md** - Context optimized for Claude
- **prompts-templates.md** - Ready-to-use prompts for common tasks

## 💡 Usage

Different AI tools read context differently:

| Tool | Reads | Priority |
|------|-------|----------|
| **GitHub Copilot** | `.github/copilot-instructions.md` | Always reads |
| **Cursor AI** | `.cursorrules` or `cursor-rules.md` | Project rules |
| **Claude** | Attach `claude-context.md` | Manual attach |
| **ChatGPT** | Copy/paste from `context.md` | Manual |
| **Other** | Read root `AI-CONTEXT.md` | Universal |

## 🎯 When to Use Each

- **Quick questions:** Use root `AI-CONTEXT.md`
- **Deep coding:** Use `cursor-rules.md` (if using Cursor)
- **Documentation:** Use `context.md`
- **Specific task:** Use `prompts-templates.md`

---

**Tip:** Most AI assistants work best with the root `AI-CONTEXT.md` + their specific file here.
