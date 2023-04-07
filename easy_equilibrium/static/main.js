
function downloadTxtFile() {
    var selectedOption = document.getElementById("dropdown").value;
    var link = document.createElement('a');
    link.setAttribute('download', selectedOption + '.txt');
    link.setAttribute('href', 'static/data/' + selectedOption + '.txt');
    link.click();
}
