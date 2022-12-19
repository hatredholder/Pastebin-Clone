$(document).ready(function(){
	var code = $(".codemirror-textarea")[0];
	var editor = CodeMirror.fromTextArea(code, {
		lineNumbers : false,
    mode: "javascript",
    theme: "material-darker"
	});
});
