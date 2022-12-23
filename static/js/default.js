// Default options for CodeMirror
var code = $(".codemirror-textarea")[0];
var editor = CodeMirror.fromTextArea(code, {
  lineNumbers : false,
  mode: "None",
  theme: "material-darker"
});

// cdnjs.com available language modes
available = ["apl", "asciiarmor", "asn.1", "asterisk", "brainfuck", "clike", "clojure", "cmake", "cobol", "coffeescript", "commonlisp", "crystal", "css", "cypher", "d", "dart", "diff", "django", "dockerfile", "dtd", "dylan", "ebnf", "ecl", "eiffel", "elm", "erlang", "factor", "fcl", "forth", "fortran", "gas", "gfm", "gherkin", "go", "groovy", "haml", "handlebars", "haskell-literate", "haskell", "haxe", "htmlembedded", "htmlmixed", "http", "idl", "javascript", "jinja2", "jsxx", "julia", "livescript", "lua", "markdown", "mathematica", "mbox", "mirc", "mllike", "modelica", "mscgen", "mumps", "nginx", "nsis", "ntriples", "octave", "oz", "pascal", "pe", "perl", "php", "pig", "powershell", "properties", "protobuf", "pug", "puppet", "python", "q", "r", "rpm", "rst", "ruby", "rust", "sas", "sass", "scheme", "shell", "sieve", "slim", "smalltalk", "smarty", "solr", "soy", "sparql", "spreadsheet", "sql", "stex", "stylus", "swift", "tcl", "textile", "tiddlywiki", "tiki", "toml", "tornado", "troff", "ttcn-cfg", "ttcn", "turtle", "twig", "vb", "vbscript", "velocity", "verilog", "vhdl", "vue", "wast", "webidl", "xml", "xquery", "yacas", "yaml-frontmatter", "yaml", "z80"]

// On selected option
$('select').on('change', function (e) {
    var cm = $(".CodeMirror")[0];
  	var code = $(".codemirror-textarea")[0];

    var valueSelected = this.value;

    // Create an id of selected option
    let id = `${valueSelected}`

    // If script with id doesn't exist yet - create it
    if(document.getElementById(id) === null) {
      // Check if selected value is available
      if(available.includes(valueSelected)){
        let script = document.createElement('script')
        script.setAttribute('src', `https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/mode/${valueSelected}/${valueSelected}.min.js`)
        script.setAttribute('id', id)
        document.body.appendChild(script) 

        // Set editor to selected option when script is loaded
        script.onload = () => {
            editor.setOption("mode", valueSelected);
        }      
      }
    }
});

