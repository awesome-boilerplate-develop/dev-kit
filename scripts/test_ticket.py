"""Tests for ticket.py without network: the HTML converter, links and keys, settings, credentials, and full
fetches against recorded-shape Azure DevOps and Jira answers.
Usage: python3 scripts/test_ticket.py"""
import importlib.util
import os
import pathlib
import re
import sys
import tempfile
import unittest
import urllib.request
from unittest import mock

spec = importlib.util.spec_from_file_location("ticket", pathlib.Path(__file__).resolve().parent / "ticket.py")
ticket = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ticket)

PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 20
GUID1 = "aaaaaaaa-0000-0000-0000-000000000001"
ADO = "https://dev.azure.com/org/Proj"


def md(fragment):
    seen = []
    out = ticket.Markdown(lambda src: seen.append(src) or f"images/{len(seen)}.png").convert(fragment)
    return out, seen


class Converter(unittest.TestCase):
    def test_inline_marks_keep_spaces_outside(self):
        out, _ = md("<div>[<b>Prescription </b>] and <i>x</i><b></b></div>")
        self.assertEqual(out, "[**Prescription** ] and *x*")

    def test_lists_nested_and_numbered(self):
        out, _ = md("<ol><li>one<ul><li>a</li><li>b</li></ul></li><li>two</li></ol>")
        self.assertEqual(out, "1. one\n   - a\n   - b\n2. two")

    def test_table_cells_keep_lines_and_escape_pipes(self):
        out, _ = md("<table><tr><td>Step</td><td>Result</td></tr><tr><td><p>Open</p><p>then</p></td>"
                    "<td>a | b</td></tr></table>")
        self.assertEqual(out, "| Step | Result |\n|---|---|\n| Open<br>then | a \\| b |")

    def test_images_numbered_in_document_order(self):
        out, seen = md('<p>x<img src="u1" alt="A"></p><p><img src="u2"></p>')
        self.assertEqual(seen, ["u1", "u2"])
        self.assertIn("![A](images/1.png)", out)
        self.assertLess(out.index("images/1"), out.index("images/2"))

    def test_code_links_rules_and_emoticons(self):
        out, seen = md('<pre>a  b\n  c</pre><hr><a href="http://x">site</a> <img class="emoticon" src="s.png" alt=":)">'
                       '<a href="/browse/A-1"><img class="icon" src="https://s/rest/api/2/universal_avatar/view/type/'
                       'issuetype/avatar/1">A-1</a>')
        self.assertIn("```\na  b\n  c\n```", out)
        self.assertIn("---", out)
        self.assertIn("[site](http://x) :)", out)
        self.assertEqual(seen, [])

    def test_jira_plus_signs_rendered_as_ins(self):
        # Jira renders "a + b + c" in a rich field as <ins> across tags; the plus signs must survive.
        out, _ = md("<p><tt>a</tt> <b><ins></b> <tt>b</tt> <b></ins></b> <tt>c</tt></p>")
        self.assertEqual(out, "`a` **+** `b` **+** `c`")


class Refs(unittest.TestCase):
    def test_links(self):
        self.assertEqual(ticket.parse_ref(f"{ADO}/_workitems/edit/1234", {}),
                         {"provider": "azure", "org": "org", "project": "Proj", "key": "1234"})
        self.assertEqual(ticket.parse_ref("https://org.visualstudio.com/Proj/_workitems/edit/7", {})["org"], "org")
        self.assertEqual(ticket.parse_ref("https://acme.atlassian.net/browse/PROJ-42", {}),
                         {"provider": "jira", "site": "acme.atlassian.net", "key": "PROJ-42"})
        self.assertEqual(ticket.parse_ref("https://acme.atlassian.net/jira/software/projects/PROJ/boards/1"
                                          "?selectedIssue=PROJ-7", {})["key"], "PROJ-7")

    def test_bare_keys_need_settings(self):
        self.assertEqual(ticket.parse_ref("#12", {"provider": "azure", "org": "o", "project": "p"})["key"], "12")
        self.assertEqual(ticket.parse_ref("proj-3", {"provider": "jira", "site": "s"})["key"], "PROJ-3")
        for bad in ("12", "PROJ-3", "hello"):
            with self.assertRaises(ticket.Fail):
                ticket.parse_ref(bad, {})

    def test_link_to_another_board_stops(self):
        with self.assertRaisesRegex(ticket.Fail, "not fetched"):
            ticket.parse_ref("https://dev.azure.com/other/P/_workitems/edit/1", {"provider": "azure", "org": "org"})
        with self.assertRaisesRegex(ticket.Fail, "not fetched"):
            ticket.parse_ref("https://b.atlassian.net/browse/A-1", {"provider": "jira", "site": "a.atlassian.net"})
        with self.assertRaisesRegex(ticket.Fail, "not fetched"):
            ticket.parse_ref("https://a.atlassian.net/browse/A-1", {"provider": "azure", "org": "org"})


class Settings(unittest.TestCase):
    def test_ticket_section_only(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d, "config.yml")
            p.write_text("commands:\n  test: make\nticket:\n  provider: jira   # board\n  site: 'a.atlassian.net'\n"
                         "  tenant:\n  types: { Bug: bug-fixer, Tech Debt: code-refactor }\nbase_branch: main\n")
            self.assertEqual(ticket.read_config(p), {"provider": "jira", "site": "a.atlassian.net",
                                                     "types": {"Bug": "bug-fixer", "Tech Debt": "code-refactor"}})


class Credentials(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = pathlib.Path(self.dir.name, ".dev-kit", "credentials.json")
        self.patch = mock.patch.object(ticket, "credentials_path", lambda: self.path)
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        self.dir.cleanup()

    def test_saved_owner_only(self):
        ticket.save_credential("jira:a.atlassian.net", {"type": "api_key", "email": "e", "key": "k"})
        ticket.save_credential("azure:org", {"type": "pat", "key": "p"})
        self.assertEqual(set(ticket.load_credentials()), {"jira:a.atlassian.net", "azure:org"})
        if os.name == "posix":
            self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)

    def test_lookup_order(self):
        ticket.save_credential("jira:a.atlassian.net", {"type": "api_key", "email": "file", "key": "k"})
        ticket.save_credential("jira:work", {"type": "api_key", "email": "profile", "key": "k"})
        env = {"JIRA_EMAIL": "env", "JIRA_API_TOKEN": "t"}
        self.assertEqual(ticket.jira_auth("a.atlassian.net", None, env).header, ticket.basic("env", "t"))
        self.assertEqual(ticket.jira_auth("a.atlassian.net", None, {}).header, ticket.basic("file", "k"))
        self.assertEqual(ticket.jira_auth("a.atlassian.net", "work", {}).header, ticket.basic("profile", "k"))
        with self.assertRaisesRegex(ticket.Fail, "id.atlassian.com/manage-profile/security/api-tokens.*login jira --site b.atlassian.net"):
            ticket.jira_auth("b.atlassian.net", None, {})

    def test_ado_pat_before_az(self):
        self.assertEqual(ticket.ado_auth("org", None, None, {"AZURE_DEVOPS_EXT_PAT": "x"}).header, ticket.basic("", "x"))
        ticket.save_credential("azure:org", {"type": "pat", "key": "p"})
        self.assertEqual(ticket.ado_auth("org", None, None, {}).header, ticket.basic("", "p"))
        with mock.patch.object(ticket, "az_token", return_value="Bearer az") as az:
            a = ticket.ado_auth("other", None, "tid", {})
            self.assertEqual(a.header, "Bearer az")
            az.assert_called_with("tid")

    def test_wrong_tenant_names_the_login(self):
        done = mock.Mock(returncode=0, stdout="t-other\n")
        with mock.patch.object(ticket.subprocess, "run", return_value=done):
            with self.assertRaisesRegex(ticket.Fail, "az login --tenant t-mine"):
                ticket.az_token("t-mine")


class Fake:
    """Answers board URLs from a table of (regex, answer); answer may be a function of the match."""

    def __init__(self, routes):
        self.routes, self.calls = routes, []

    def __call__(self, url, auth, body=None, raw=False):
        self.calls.append((url, body))
        for pattern, answer in self.routes:
            m = re.search(pattern, url)
            if m:
                return answer(m) if callable(answer) else answer
        raise AssertionError(f"unexpected request {url}")


def ado_routes():
    att = f"{ADO}/_apis/wit/attachments"
    items = {
        "100": {"id": 100, "fields": {
            "System.WorkItemType": "Bug", "System.Title": "Drug name issues", "System.State": "Active",
            "System.Tags": "ui; rx", "System.AssignedTo": {"displayName": "Dev"},
            "System.Description": f'<div><b>Bug 1</b> wrong</div><div><img src="{att}/{GUID1}?fileName=image.png"></div>',
            "Microsoft.VSTS.TCM.ReproSteps": "<table><tr><td>Step</td><td>Result</td></tr><tr><td>1.</td><td>Failed</td></tr></table>",
            "Microsoft.VSTS.TCM.SystemInfo": "<p>hidden on this form</p>"},
            "relations": [
                {"rel": "System.LinkTypes.Related", "url": "https://dev.azure.com/org/_apis/wit/workItems/200",
                 "attributes": {"name": "Related"}},
                {"rel": "AttachedFile", "url": f"{att}/bbbbbbbb-0000-0000-0000-000000000002",
                 "attributes": {"name": f"{GUID1}.png", "resourceSize": 30}},
                {"rel": "AttachedFile", "url": f"{att}/cccccccc-0000-0000-0000-000000000003",
                 "attributes": {"name": "spec.xlsx", "resourceSize": 2048}},
                {"rel": "ArtifactLink", "url": "vstfs:///Git/PullRequestId/pid%2Frepo1%2F42",
                 "attributes": {"name": "Pull Request"}}]},
        "10": {"id": 10, "fields": {
            "System.WorkItemType": "User Story", "System.Title": "Override reason per row", "System.State": "Active",
            "System.Parent": 1, "System.Description": "<p>As a doctor</p>",
            "Microsoft.VSTS.Common.AcceptanceCriteria": "<ol><li>Finalize disabled</li></ol>"},
            "relations": [{"rel": "System.LinkTypes.Hierarchy-Forward", "url": f"https://dev.azure.com/org/_apis/wit/workItems/{i}",
                           "attributes": {}} for i in (11, 12)]},
        "11": {"id": 11, "fields": {"System.WorkItemType": "Task", "System.Title": "[DEV] FE Development",
                                    "System.State": "To Do", "System.Parent": 10}},
        "12": {"id": 12, "fields": {"System.WorkItemType": "Task", "System.Title": "[DEV] BE Development",
                                    "System.State": "Done", "System.Parent": 10, "System.Description": "<p>API /rx</p>"}},
    }
    briefs = {"1": ("Feature", "Rx", "New"), "10": ("User Story", "Override reason per row", "Active"),
              "11": ("Task", "[DEV] FE Development", "To Do"), "12": ("Task", "[DEV] BE Development", "Done"),
              "200": ("Bug", "Other bug", "Closed")}
    forms = {"Bug": ["System.Description", "Microsoft.VSTS.TCM.ReproSteps"],
             "User Story": ["System.Description", "Microsoft.VSTS.Common.AcceptanceCriteria"],
             "Task": ["System.Description"]}

    def brief(m):
        return {"value": [{"id": int(i), "fields": {"System.WorkItemType": briefs[i][0], "System.Title": briefs[i][1],
                                                    "System.State": briefs[i][2]}} for i in m.group(1).split(",")]}

    def layout(m):
        labels = {"System.Description": "Description", "Microsoft.VSTS.TCM.ReproSteps": "Repro Steps",
                  "Microsoft.VSTS.Common.AcceptanceCriteria": "Acceptance Criteria"}
        controls = [{"id": f, "label": labels[f], "controlType": "HtmlFieldControl"} for f in forms[m.group(1)]]
        return {"pages": [{"visible": True, "sections": [{"groups": [{"label": "g", "controls": controls}]}]}]}

    comments = {"100": [{"createdBy": {"displayName": "QA"}, "createdDate": "2026-10-02T07:47:00Z", "renderedText": "<div>newest</div>"},
                        {"createdBy": {"displayName": "QA"}, "createdDate": "2026-10-01T04:49:00Z", "text": "older"}]}
    return [
        (r"/_apis/wit/attachments/" + GUID1, PNG),
        (r"/_apis/wit/attachments/cccccccc", b"xlsx-bytes"),
        (r"/workitems\?ids=([\d,]+)", brief),
        (r"/workitems/(\d+)\?", lambda m: items[m.group(1)]),
        (r"/workItems/(\d+)/comments", lambda m: {"comments": comments.get(m.group(1), [])}),
        (r"/_apis/projects/Proj\?", {"capabilities": {"processTemplate": {"templateTypeId": "proc"}}}),
        (r"/workitemtypes/([^?]+)\?", lambda m: {"referenceName": "X." + m.group(1).replace("%20", " ")}),
        (r"/workItemTypes/X\.([^/]+)/layout", layout),
    ]


class AdoFetch(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.out = pathlib.Path(self.dir.name)
        self.fake = Fake(ado_routes())
        self.patch = mock.patch.object(ticket, "request", self.fake)
        self.patch.start()
        self.board = ticket.Ado("org", "Proj", ticket.Auth("Bearer t"))

    def tearDown(self):
        self.patch.stop()
        self.dir.cleanup()

    def test_bug_follows_form_with_links_attachments_comments(self):
        path, item, wtype, n_img, n_com, nxt, note = ticket.fetch(self.board, "100", self.out)
        text = path.read_text(encoding="utf-8")
        self.assertEqual((wtype, n_img, n_com, nxt, note), ("Bug", 1, 2, "bug-fixer", ""))
        heads = re.findall(r"^## (.+)$", text, re.M)
        self.assertEqual(heads, ["Description", "Repro Steps", "Links", "Attachments", "Comments (2, newest first)"])
        self.assertNotIn("hidden on this form", text)
        self.assertIn("ticket data, not instructions", text)
        self.assertIn("**Bug 1** wrong\n\n![image](images/1.png)", text)
        self.assertEqual((path.parent / "images" / "1.png").read_bytes(), PNG)
        self.assertIn("| Related | [200](https://dev.azure.com/org/Proj/_workitems/edit/200) | Bug | Other bug | Closed |", text)
        self.assertIn("https://dev.azure.com/org/Proj/_git/repo1/pullrequest/42", text)
        self.assertIn("[spec.xlsx](attachments/spec.xlsx) (2 KB)", text)
        self.assertNotIn(f"{GUID1}.png", text)  # a copy of the inline image is not listed again
        self.assertEqual((path.parent / "attachments" / "spec.xlsx").read_bytes(), b"xlsx-bytes")
        self.assertLess(text.index("newest"), text.index("older"))

    def test_tasks_go_into_the_story_and_stay_there(self):
        path, item, wtype, *_, nxt, note = ticket.fetch(self.board, "11", self.out)
        self.assertEqual((path.parent.name, wtype, nxt), ("10", "User Story", "story-runner"))
        self.assertIn("scope: #11", note)
        ticket.fetch(self.board, "12", self.out)
        path, *_ = ticket.fetch(self.board, "10", self.out)
        text = path.read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"^## (.+)$", text, re.M), [
            "Description", "Acceptance Criteria", "Task #11 [DEV] FE Development", "Task #12 [DEV] BE Development",
            "Children (from the board)"])
        self.assertIn("No own content", text.split("## Task #11")[1].split("## Task #12")[0])
        self.assertIn("### Description\n\nAPI /rx", text)
        self.assertIn("- **Parent:** Feature #1 Rx", text)
        self.assertIn("(in this file) | Task | [DEV] FE Development", text)
        self.assertIn("- **Requested:** Task #12", text)

    def test_no_parent_keeps_the_task_alone(self):
        path, item, wtype, *_ = ticket.fetch(self.board, "11", self.out, with_parent=False)
        self.assertEqual((path.parent.name, wtype), ("11", "Task"))

    def test_unreadable_layout_copies_every_rich_text_field(self):
        self.fake.routes.insert(0, (r"/layout", lambda m: (_ for _ in ()).throw(ticket.Fail("403"))))
        path, *_ = ticket.fetch(self.board, "100", self.out)
        self.assertIn("hidden on this form", path.read_text(encoding="utf-8"))

    def test_query_writes_an_index(self):
        self.fake.routes.insert(0, (r"/wiql", {"workItems": [{"id": 100}]}))
        cfg = {"provider": "azure", "org": "org", "project": "Proj"}
        cwd = os.getcwd()
        os.chdir(self.dir.name)
        try:
            with mock.patch.object(ticket, "board", lambda ref, c, e: self.board), mock.patch("builtins.print"):
                self.assertEqual(ticket.cmd_query(["SELECT 1", "--limit", "5"], cfg, {}), 0)
            index = next(pathlib.Path(".dev-kit/tickets").glob("index-*.md")).read_text(encoding="utf-8")
            self.assertTrue(pathlib.Path(".dev-kit/.gitignore").read_text(encoding="utf-8").startswith("*"))
        finally:
            os.chdir(cwd)
        self.assertIn("| [#100](100/ticket.md) | Bug | Drug name issues | Active | dk:bug-fixer |", index)
        self.assertEqual(self.fake.calls[0][1], {"query": "SELECT 1"})


def jira_routes():
    site = "https://acme.atlassian.net"
    issues = {
        "PROJ-1": {"key": "PROJ-1",
                  "names": {"description": "Description", "customfield_100": "Acceptance Criteria", "customfield_5": "Sprint"},
                  "renderedFields": {
                      "description": '<p>Story text <span class="image-wrap"><img src="/secure/thumbnail/10001/a.png"></span></p>',
                      "customfield_100": "<ul><li>AC one</li></ul>",
                      "comment": {"comments": [{"id": "1", "body": "<p>first</p>"}, {"id": "2", "body": f'<p>second</p><p><img src="{site}/rest/api/3/attachment/content/10003"></p>'}]}},
                  "fields": {"issuetype": {"name": "Story", "subtask": False}, "summary": "Checkout", "status": {"name": "In Progress"},
                             "assignee": {"displayName": "Ann"}, "labels": ["web"], "customfield_5": [{"name": "Sprint 5"}],
                             "attachment": [{"id": 10001, "filename": "a.png", "size": 100, "content": f"{site}/rest/api/3/attachment/content/10001"},
                                            {"id": 10002, "filename": "doc.pdf", "size": 4096, "content": f"{site}/rest/api/3/attachment/content/10002"},
                                            {"id": 10003, "filename": "shot.png", "size": 100, "content": f"{site}/rest/api/3/attachment/content/10003"}],
                             "issuelinks": [{"type": {"inward": "is blocked by", "outward": "blocks"},
                                             "outwardIssue": {"key": "PROJ-2", "fields": {"summary": "Pay", "status": {"name": "To Do"},
                                                                                       "issuetype": {"name": "Story"}}}}],
                             "comment": {"comments": [{"id": "1", "author": {"displayName": "Bo"}, "created": "2026-01-01T10:00:00.000+0000"},
                                                      {"id": "2", "author": {"displayName": "Cy"}, "created": "2026-01-02T10:00:00.000+0000"}]}}},
        "PROJ-3": {"key": "PROJ-3", "names": {}, "renderedFields": {"description": "<p>Do the FE part</p>"},
                  "fields": {"issuetype": {"name": "Sub-task", "subtask": True}, "summary": "FE", "status": {"name": "To Do"},
                             "parent": {"key": "PROJ-1", "fields": {"summary": "Checkout", "issuetype": {"name": "Story"}}}}},
    }
    return [
        (r"/rest/api/3/attachment/content/10001", PNG),
        (r"/rest/api/3/attachment/content/10002", b"%PDF"),
        (r"/rest/api/3/attachment/content/10003", PNG),
        (r"/issue/([A-Z]+-\d+)/remotelink", lambda m: [{"relationship": "mentioned in",
                                                        "object": {"url": "https://git.example/pr/1", "title": "PR 1"}}]
         if m.group(1) == "PROJ-1" else []),
        (r"/issue/([A-Z]+-\d+)\?", lambda m: issues[m.group(1)]),
        (r"/search/jql\?jql=parent", {"issues": [{"key": "PROJ-3", "fields": {"summary": "FE", "status": {"name": "To Do"},
                                                                             "issuetype": {"name": "Sub-task"}}}]}),
    ]


class JiraFetch(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.out = pathlib.Path(self.dir.name)
        self.patch = mock.patch.object(ticket, "request", Fake(jira_routes()))
        self.patch.start()
        self.board = ticket.Jira("acme.atlassian.net", ticket.Auth("Basic x"), "customfield_100")

    def tearDown(self):
        self.patch.stop()
        self.dir.cleanup()

    def test_story(self):
        path, item, wtype, n_img, n_com, nxt, _ = ticket.fetch(self.board, "PROJ-1", self.out)
        text = path.read_text(encoding="utf-8")
        self.assertEqual((wtype, n_img, n_com, nxt), ("Story", 2, 2, "story-runner"))
        self.assertNotIn("[shot.png]", text)  # shown in a comment, which is converted before the attachments list
        self.assertLess(text.index("second"), text.index("images/2.png"))
        self.assertEqual(re.findall(r"^## (.+)$", text, re.M),
                         ["Description", "Acceptance Criteria", "Links", "Attachments", "Comments (2, oldest first)"])
        self.assertIn("- **Sprint:** Sprint 5", text)
        self.assertIn("| blocks | [PROJ-2](https://acme.atlassian.net/browse/PROJ-2) | Story | Pay | To Do |", text)
        self.assertIn("[PR 1](https://git.example/pr/1)", text)
        self.assertIn("[doc.pdf](attachments/doc.pdf)", text)
        self.assertNotIn("[a.png]", text)  # shown inline already
        self.assertEqual((path.parent / "images" / "1.png").read_bytes(), PNG)
        self.assertLess(text.index("first"), text.index("second"))

    def test_subtask_goes_into_its_story(self):
        path, item, wtype, *_, nxt, note = ticket.fetch(self.board, "PROJ-3", self.out)
        text = path.read_text(encoding="utf-8")
        self.assertEqual((path.parent.name, wtype, nxt), ("PROJ-1", "Story", "story-runner"))
        self.assertIn("## Sub-task PROJ-3 FE", text)
        self.assertIn("### Description\n\nDo the FE part", text)
        self.assertIn("| [PROJ-3](https://acme.atlassian.net/browse/PROJ-3) (in this file) | Sub-task | FE | To Do |", text)


class Plumbing(unittest.TestCase):
    def test_next_skill(self):
        it = lambda t, **kw: ticket.Item(type=t, **kw)
        self.assertEqual(ticket.next_skill(it("Bug"), None), "bug-fixer")
        self.assertEqual(ticket.next_skill(it("Bug"), {"Bug": "story-runner"}), "story-runner")
        self.assertEqual(ticket.next_skill(it("Task", labels=["Tech-Debt"]), None), "code-refactor")
        self.assertEqual(ticket.next_skill(it("User Story", sections=[("Acceptance Criteria", "<p>x</p>")]), None), "story-runner")
        self.assertEqual(ticket.next_skill(it("Story", sections=[("Description", "<p>tbd</p>")]), None), "brainstorm")
        self.assertEqual(ticket.next_skill(it("Task"), None), "?")

    def test_401_retries_once_with_a_fresh_token(self):
        calls = []

        def fake(url, auth, body=None, raw=False):
            calls.append(auth)
            if auth == "old":
                raise ticket.Unauthorized("401")
            return {"ok": True}

        with mock.patch.object(ticket, "request", fake):
            b = ticket.Board(ticket.Auth("old", refresh=lambda: "new"))
            self.assertEqual(b.get("u"), {"ok": True})
            self.assertEqual(calls, ["old", "new"])
            with self.assertRaisesRegex(ticket.Fail, "run login"):
                ticket.Board(ticket.Auth("old", hint="run login")).get("u")

    def test_redirect_to_another_host_drops_the_token(self):
        h = ticket.SameHostAuth()
        req = urllib.request.Request("https://acme.atlassian.net/a", headers={"Authorization": "Basic x"})
        same = h.redirect_request(req, None, 302, "", {}, "https://acme.atlassian.net/b")
        other = h.redirect_request(req, None, 302, "", {}, "https://media.example/b")
        self.assertIn("Authorization", same.headers)
        self.assertNotIn("Authorization", other.headers)

    def test_sha_ignores_the_fetch_time(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = pathlib.Path(d, "a.md"), pathlib.Path(d, "b.md")
            a.write_text("# T\n- **Fetched:** 2026-01-01 10:00\nbody\n")
            b.write_text("# T\n- **Fetched:** 2026-02-02 11:00\nbody\n")
            self.assertEqual(ticket.content_sha(a), ticket.content_sha(b))

    def test_translations_current_or_stale(self):
        with tempfile.TemporaryDirectory() as d:
            src = pathlib.Path(d, "ticket.md")
            src.write_text("# T\n- **Fetched:** now\nbody\n", encoding="utf-8")
            sha = ticket.content_sha(src)
            pathlib.Path(d, "ticket.vi.md").write_text(f"> Translation of ticket.md · sha {sha} · d\n", encoding="utf-8")
            pathlib.Path(d, "ticket.ja.md").write_text("> Translation · sha 000000000000 · d\n", encoding="utf-8")
            self.assertEqual(ticket.translations(src, sha), ["ja:stale", "vi:current"])
        self.assertEqual(ticket.translate_line({"translate": "vi"}), "translate=vi")
        self.assertTrue(ticket.translate_line({}).startswith("translate=ask"))

    def test_home_folder_refused(self):
        with tempfile.TemporaryDirectory() as d:
            cwd = os.getcwd()
            os.chdir(d)
            try:
                with mock.patch.object(ticket.pathlib.Path, "home", lambda: pathlib.Path(d)):
                    with self.assertRaisesRegex(ticket.Fail, "home folder"):
                        ticket.prepare_out(pathlib.Path(".dev-kit/tickets"))
            finally:
                os.chdir(cwd)

    def test_login_refuses_without_a_terminal(self):
        with mock.patch.object(sys.stdin, "isatty", lambda: False):
            with self.assertRaisesRegex(ticket.Fail, "terminal"):
                ticket.cmd_login(["jira", "--site", "a.atlassian.net"], {}, {})


if __name__ == "__main__":
    unittest.main()
