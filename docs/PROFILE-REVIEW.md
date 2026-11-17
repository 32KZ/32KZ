# Profile README review

Reviewed on 17 November 2026, against the public `32KZ/32KZ` README at commit `4fb6153`.

## Readability changes

- Give each subject one clear home instead of repeating it across the intro, current work, and featured projects.
- Add short navigation links and consistent second- and third-level headings.
- Replace the all-caps feature paragraph with scannable bullets.
- Fix spelling, punctuation, and inconsistent project names while keeping the informal voice and the original tagline.
- Move ZEKE-UI into a collapsed **Older stuff** section at the bottom, including all three screenshots.
- Give Minecraft its own client and server subsections.
- Leave SUPERNOVA as a heading and successor label, ready for a new description, as requested.
- Separate languages from Electron, and place TCP/IP with networking.
- Add useful alternative text to the existing graphics.
- Replace the absolute "bug free" claim with a description of the interface. Treat the two version numbers as historical notes rather than a current release claim.
- Replace the empty "Featured Projects" heading and access joke with the actual project sections. Preserve the private-project status and eventual open-source intention in the archive.

## Complete content inventory

These categories cover the subjects, named tools, and media in the original README. Placement follows the requested split; it does not assert that every listed feature is finished or current.

| Category | Everything mentioned in the original | Placement |
| --- | --- | --- |
| Identity & focus | Automation systems; game/server tooling; reliability; security; building exactly what is needed; "See cool shit → Think cool shit → Build cool shit" | Main introduction |
| SUPERNOVA | Windows application; successor inheriting ZEKE-UI functionality; Shift+Alt+Space shortcut; Raycast-like, always-on-top display; AI control | Blank main section with successor label. The previous feature description is retained in this inventory for reuse. |
| ZEKE-UI: identity & status | Windows workspace; eDEX-UI and CoLateral influences; richer feature set; customisable theme; integrated JARVIS-style assistant; inbuilt desktop; pop-out windows; widget shortcuts; slowed development; repurposing into SUPERNOVA; private access; possible eventual open-source release | Older stuff |
| ZEKE-UI: widgets | 14 widgets; files; Monaco programming editor; projects with building support; task manager; terminal; Git Bash, WSL, CMD, PowerShell; terminals connected to the active files widget; global situation view | Older stuff |
| ZEKE-UI: workspace design | Unlimited workspaces; create, rename, reorder, export; modular widget structure; user-defined expansion; ten random startup splashes; configurable splashes following a persistent theme | Older stuff |
| ZEKE-UI: AI | NOVA AI; voice and text control; "ruflow" swarm orchestration; realtime speech model | Older stuff |
| Mobile & XR | Mobile app to dispatch work; "sleep bluetooth connectivity" with headphones; always-in-ear support; XR glasses; EDITH-style control | Older stuff, described as the original direction |
| ZEKE-UI: history & media | v0.16.34; later v0.22.71; three development screenshots | Older stuff, labeled as historical |
| Minecraft: client | ZEEK-PACKET; Minecraft 1.21.1; Meteor addon; tools from Autism Client and UIUtils; custom modules; client-side enrichment/development | Dedicated Minecraft section |
| Minecraft: server | Paper/Spigot plugins; custom server tooling; permissions; LuckPerms; performance; stability; Gradle/Maven; TCP/IP | Dedicated Minecraft section and skill table |
| Automation & AI integrations | n8n; Docker workflows; AI integrations; production automation patterns; workflow templates; credential-safe design; webhooks; API integrations | Dedicated Automation section |
| Languages & application tools | C#; Java; Python; JavaScript; TypeScript; Electron; HTML5 badge | Skill table; existing badges retained |
| APIs, data & infrastructure | REST APIs; webhooks; OAuth; Postgres/PostgreSQL; Docker; Linux; Nginx; GitHub Actions | Skill table; relevant automation tools also appear in Automation |
| Principles | Common sense; consolidating control for the end user; "IM THE DEV" | Main Principles section |
| Contact | Email available on request; Discord 32KZ | Main Contact section |
| Visual identity | Existing banner; C#, Java, Meteor, n8n, HTML5 badges | Main header, with alt text |
| Repository boilerplate | Hidden explanation of why the username repository appears on the GitHub profile | Removed template comment |

### Details worth confirming when updating the archive

- The original spells the swarm tool **ruflow**. That spelling is preserved; confirm the intended product name before changing it.
- "Sleep bluetooth connectivity" has been clarified to low-power Bluetooth connectivity. Confirm that this captures the intended behaviour.
- The original does not separate implemented mobile/XR features from ideas. The archive calls this a direction rather than claiming a shipped app.
- The screenshots did not identify which version each depicts. No new version-to-image mapping has been invented.
- SUPERNOVA's old shortcut and UI description are intentionally absent from the blank main section; they remain in the inventory above.

## Widget suggestions

Pick one or two extras so the profile stays readable. Only the requested contribution calendar has been added.

| Widget | Why it fits | Source / setup |
| --- | --- | --- |
| Compact project status panel | Best fit: show SUPERNOVA as ZEKE-UI's successor, ZEEK-PACKET's Minecraft version, and whether each project is private. Update the labels manually so they stay honest. | Native Markdown table or locally stored SVG; no external service required. Add SUPERNOVA details when ready. |
| Contribution snake | A playful animation using the same contribution grid. Best placed near the bottom so it doesn't compete with the new calendar. | [Platane/snk](https://github.com/Platane/snk), generated with GitHub Actions. |
| Consistent skill icon strip | A cleaner visual row for C#, Java, Python, TypeScript, Electron, Docker, and Linux. Use this as a replacement for the existing badges if desired. | [Skill Icons](https://github.com/tandpfun/skill-icons). |
| One compact metrics card | Useful for a recent activity or language breakdown without stacking multiple statistics panels. Public-repository language percentages describe repository code, not skill level, and will miss private project code. | [lowlighter/metrics](https://github.com/lowlighter/metrics). Choose just the relevant modules. |
| Public release / build badges | Useful on individual public projects once there is a release or workflow worth following. Avoid badges that imply visitors can access private repos. | [Shields.io](https://shields.io/badges) for project-specific badges. |

Optional skill strip (not added):

```md
[![C#, Java, Python, JavaScript, TypeScript, Electron, Docker, Linux](https://skillicons.dev/icons?i=cs,java,py,js,ts,electron,docker,linux&perline=8)](https://skillicons.dev)
```

My suggested combination is **the contribution calendar + one small project status panel**. A snake can be an optional footer flourish. Another general activity graph would duplicate the calendar.

## Contribution calendar maintenance

- `assets/contributions-dark.svg` matches the supplied screenshot's 1367 × 332 layout: title, rounded border, months, weekday labels, green cells, and legend. A light version is selected through the README's `picture` element.
- The initial images use the real public calendar downloaded on 17 November 2026: **83 contributions**, spanning **16 November 2025–17 November 2026** (367 displayed days, including GitHub's leading week alignment).
- The generator reads the public calendar without a token. It reflects whatever activity GitHub exposes publicly, including anonymised private activity if enabled in the profile settings; it does not inspect private repositories.
- Images are static snapshots. The full image links to the native profile calendar; GitHub's interactive day selection is not replicated inside the README image. The footer's help text is decorative as part of the replica.
- `.github/workflows/contributions.yml` refreshes both files daily at **03:27 UTC**, on manual dispatch, and when its generator/workflow changes on `main`. Scheduled runs begin after this workflow reaches the default branch. GitHub can delay scheduled runs and image caching can delay visible updates.
- The refresh job uses the built-in `GITHUB_TOKEN` with `contents: write` to commit only the two SVGs. No personal access token or third-party widget host is needed. Protected branch rules may require adjusting the commit strategy.
- The unit tests run on relevant pull requests without write permission. The parser checks complete dates, tooltip counts, contribution levels, and the displayed total before replacing existing images. If GitHub changes its HTML, it fails visibly and retains the previous images.
- The full-year calendar scales to the README width. Its tiny daily squares are best inspected through the linked native calendar on a phone.

```sh
python scripts/contributions.py --user 32KZ
python -m unittest discover -s scripts -p 'test_*.py' -v
```

References: [GitHub profile READMEs](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme), [contribution calendars](https://docs.github.com/en/account-and-profile/how-tos/contribution-settings/viewing-contributions-on-your-profile), [workflow token permissions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token).
