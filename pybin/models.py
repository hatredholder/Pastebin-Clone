import datetime
import uuid

from app import db


class Comment(db.EmbeddedDocument):
    content = db.StringField(max_length=300, required=True)
    author = db.ReferenceField("User", required=True)
    paste = db.ReferenceField("Paste", required=True)

    created = db.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        if len(str(self.content)) > 50:
            return f"<Comment {self.author} - {str(self.content)[:50].strip()}..>"
        return f"<Comment {self.author} - {str(self.content)}>"


CATEGORIES = (
    "None",
    "Cryptocurrency",
    "Cybersecurity",
    "Fixit",
    "Food",
    "Gaming",
    "Haiku",
    "Help",
    "History",
    "Housing",
    "Jokes",
    "Legal",
    "Money",
    "Movies",
    "Music",
    "Pets",
    "Photo",
    "Science",
    "Software",
    "Source Code",
    "Spirit",
    "Sports",
    "Travel",
    "TV",
    "Writing",
)

PASTE_EXPIRATION = (
    (0, "Never"),
    (3600, "1 Hour"),
    (86400, "1 Day"),
    (2592000, "1 Month"),
    (31104000, "1 Year"),
)

PASTE_EXPOSURE = (
    "Public",
    "Unlisted",
    "Private",
)


SYNTAXES = (
    ("None", "None"),
    ("1c", "1C"),
    ("abnf", "ABNF"),
    ("accesslog", "Accesslogs"),
    ("ada", "Ada"),
    ("arduino", "Arduino"),
    ("armasm", "ARMassembler"),
    ("avrasm", "AVRassembler"),
    ("actionscript", "ActionScript"),
    ("angelscript", "AngelScript"),
    ("apache", "Apache"),
    ("applescript", "AppleScript"),
    ("arcade", "Arcade"),
    ("asciidoc", "AsciiDoc"),
    ("aspectj", "AspectJ"),
    ("autohotkey", "AutoHotkey"),
    ("autoit", "AutoIt"),
    ("awk", "Awk"),
    ("bash", "Bash"),
    ("basic", "Basic"),
    ("bnf", "BNF"),
    ("brainfuck", "Brainfuck"),
    ("csharp", "C#"),
    ("c", "C"),
    ("cpp", "C++"),
    ("cal", "C/AL"),
    ("cmake", "CMake"),
    ("coq", "Coq"),
    ("csp", "CSP"),
    ("css", "CSS"),
    ("capnproto", "Cap’nProto"),
    ("clojure", "Clojure"),
    ("coffeescript", "CoffeeScript"),
    ("crmsh", "Crmsh"),
    ("crystal", "Crystal"),
    ("d", "D"),
    ("dart", "Dart"),
    ("dpr", "Delphi"),
    ("diff", "Diff"),
    ("django", "Django"),
    ("dns", "DNSZonefile"),
    ("dockerfile", "Dockerfile"),
    ("dos", "DOS"),
    ("dsconfig", "dsconfig"),
    ("dust", "Dust"),
    ("ebnf", "EBNF"),
    ("elixir", "Elixir"),
    ("elm", "Elm"),
    ("erlang", "Erlang"),
    ("excel", "Excel"),
    ("fsharp", "F#"),
    ("fix", "FIX"),
    ("fortran", "Fortran"),
    ("gcode", "G-Code"),
    ("gams", "Gams"),
    ("gauss", "GAUSS"),
    ("gherkin", "Gherkin"),
    ("go", "Go"),
    ("golo", "Golo"),
    ("gradle", "Gradle"),
    ("graphql", "GraphQL"),
    ("groovy", "Groovy"),
    ("html", "XML"),
    ("http", "HTTP"),
    ("haml", "Haml"),
    ("handlebars", "Handlebars"),
    ("haskell", "Haskell"),
    ("haxe", "Haxe"),
    ("hy", "Hy"),
    ("ini", "TOML"),
    ("inform7", "Inform7"),
    ("irpf90", "IRPF90"),
    ("json", "JSON"),
    ("java", "Java"),
    ("javascript", "JavaScript"),
    ("julia", "Julia"),
    ("kotlin", "Kotlin"),
    ("tex", "LaTeX"),
    ("leaf", "Leaf"),
    ("lasso", "Lasso"),
    ("less", "Less"),
    ("ldif", "LDIF"),
    ("lisp", "Lisp"),
    ("livescript", "LiveScript"),
    ("lua", "Lua"),
    ("makefile", "Makefile"),
    ("markdown", "Markdown"),
    ("mathematica", "Mathematica"),
    ("matlab", "Matlab"),
    ("maxima", "Maxima"),
    ("mercury", "Mercury"),
    ("mizar", "Mizar"),
    ("mojolicious", "Mojolicious"),
    ("monkey", "Monkey"),
    ("moonscript", "Moonscript"),
    ("n1ql", "N1QL"),
    ("nsis", "NSIS"),
    ("nginx", "Nginx"),
    ("nim", "Nim"),
    ("nix", "Nix"),
    ("ocaml", "OCaml"),
    ("objectivec", "ObjectiveC"),
    ("openscad", "OpenSCAD"),
    ("oxygene", "Oxygene"),
    ("pf", "PF"),
    ("php", "PHP"),
    ("parser3", "Parser3"),
    ("perl", "Perl"),
    ("plaintext", "Plaintext"),
    ("pony", "Pony"),
    ("powershell", "PowerShell"),
    ("processing", "Processing"),
    ("prolog", "Prolog"),
    ("properties", "Properties"),
    ("puppet", "Puppet"),
    ("python", "Python"),
    ("python-repl", "PythonREPL"),
    ("k", "Q"),
    ("qml", "QML"),
    ("r", "R"),
    ("reasonml", "ReasonML"),
    ("rib", "RenderManRIB"),
    ("rsl", "RenderManRSL"),
    ("graph", "Roboconf"),
    ("ruby", "Ruby"),
    ("rust", "Rust"),
    ("SAS", "SAS"),
    ("scss", "SCSS"),
    ("sql", "SQL"),
    ("p21", "STEPPart21"),
    ("scala", "Scala"),
    ("scheme", "Scheme"),
    ("scilab", "Scilab"),
    ("shell", "Shell"),
    ("smali", "Smali"),
    ("smalltalk", "Smalltalk"),
    ("sml", "SML"),
    ("stan", "Stan"),
    ("stata", "Stata"),
    ("stylus", "Stylus"),
    ("subunit", "SubUnit"),
    ("swift", "Swift"),
    ("tcl", "Tcl"),
    ("thrift", "Thrift"),
    ("tp", "TP"),
    ("twig", "Twig"),
    ("typescript", "TypeScript"),
    ("vbnet", "VB.Net"),
    ("vbscript", "VBScript"),
    ("vhdl", "VHDL"),
    ("vala", "Vala"),
    ("verilog", "Verilog"),
    ("vim", "VimScript"),
    ("axapta", "X++"),
    ("x86asm", "x86Assembly"),
    ("xl", "XL"),
    ("xquery", "XQuery"),
    ("yml", "YAML"),
    ("zephir", "Zephir"),
)


class Paste(db.Document):
    content = db.StringField(max_length=512000, required=True)

    category = db.StringField(choices=CATEGORIES, required=False, default="None")
    tags = db.ListField(max_length=10, required=False)
    syntax = db.StringField(
        choices=SYNTAXES,
        required=True,
        default="None",
    )
    paste_expiration = db.IntField(choices=PASTE_EXPIRATION, required=True, default=0)
    paste_exposure = db.StringField(
        choices=PASTE_EXPOSURE,
        required=True,
        default="Public",
    )
    paste_hash = db.StringField(default=lambda: str(uuid.uuid4())[:8], primary_key=True)
    title = db.StringField(max_length=50, required=False, default="Untitled")

    author = db.ReferenceField("User", required=True, reverse_delete_rule=db.CASCADE)
    comments = db.EmbeddedDocumentListField("Comment", required=False)

    created = db.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        if len(str(self.content)) > 50:
            return f"<Paste {self.author} - {str(self.content)[:50].strip()}..>"
        return f"<Paste {self.author} - {str(self.content)}>"
