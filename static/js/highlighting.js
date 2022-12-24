// Some variables
var textarea = $(".codemirror-textarea")[0];
var toggleButton = $("#onoff")[0];


// cdnjs.com available language modes
available = ["apl", "asciiarmor", "asn.1", "asterisk", "brainfuck", "clike", "clojure", "cmake", "cobol", "coffeescript", "commonlisp", "crystal", "css", "cypher", "d", "dart", "diff", "django", "dockerfile", "dtd", "dylan", "ebnf", "ecl", "eiffel", "elm", "erlang", "factor", "fcl", "forth", "fortran", "gas", "gfm", "gherkin", "go", "groovy", "haml", "handlebars", "haskell-literate", "haskell", "haxe", "htmlembedded", "htmlmixed", "http", "idl", "javascript", "jinja2", "jsxx", "julia", "livescript", "lua", "markdown", "mathematica", "mbox", "mirc", "mllike", "modelica", "mscgen", "mumps", "nginx", "nsis", "ntriples", "octave", "oz", "pascal", "pe", "perl", "php", "pig", "powershell", "properties", "protobuf", "pug", "puppet", "python", "q", "r", "rpm", "rst", "ruby", "rust", "sas", "sass", "scheme", "shell", "sieve", "slim", "smalltalk", "smarty", "solr", "soy", "sparql", "spreadsheet", "sql", "stex", "stylus", "swift", "tcl", "textile", "tiddlywiki", "tiki", "toml", "tornado", "troff", "ttcn-cfg", "ttcn", "turtle", "twig", "vb", "vbscript", "velocity", "verilog", "vhdl", "vue", "wast", "webidl", "xml", "xquery", "yacas", "yaml-frontmatter", "yaml", "z80"]


// Create script tag and load mode into editor
function createScriptTag(id, valueSelected, editor){
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
  else {
    editor.setOption("mode", valueSelected);
  }
}


// Load language package on select if syntax highlighting is enabled
$('select').on('change', function (e) {

    // Check if syntax highlighting is enabled
    if (toggleButton.value == "on"){

      var editor = $(".CodeMirror")[0].CodeMirror
      var valueSelected = this.value;

      // Create an id of selected option
      let id = `${valueSelected}`

      // If script tag with id doesn't exist yet - create it
      createScriptTag(id, valueSelected, editor)
    }
});

// On/off toggle button
$('#onoff').on('change', function() {
    if (this.value == "off"){
      
      var valueSelected = $("#syntax")[0].value
      let id = `${valueSelected}`

      // Set value to on
      document.getElementById("onoff").value="on"

      // Setup CodeMirror
      var editor = CodeMirror.fromTextArea(textarea, {
        lineNumbers : false,
        mode: "None",
        theme: "material-darker"
      });

      // Set mode for CodeMirror from selected value
      createScriptTag(id, valueSelected, editor)
    }
    else {

      // Set value to off
      document.getElementById("onoff").value="off"
      
      // Hide CodeMirror and show textarea
      cm = $(".CodeMirror")[0].CodeMirror
      $(cm.getWrapperElement()).hide();
      $(".codemirror-textarea").show()
    }
});
