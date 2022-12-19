var code = $(".codemirror-textarea")[0];
var editor = CodeMirror.fromTextArea(code, {
  lineNumbers : false,
  mode: "None",
  theme: "material-darker"
});
$('select').on('change', function (e) {
    var cm = $(".CodeMirror")[0];
  	var code = $(".codemirror-textarea")[0];

    var valueSelected = this.value;

    editor.setOption("mode", valueSelected);
});

