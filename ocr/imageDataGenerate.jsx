imageRoundCounter = 0;
function generateTextImage(font, path){
    let layers = app.activeDocument.layers;
    // let path = app.activeDocument.path;
    let path = path != undefined ? path : '';
    console.log(path);

    function saveAs(name, type) {
        // var saveFile = new File(path + name + '/' + (imageRoundCounter++).toString() + '.' + type);
        var saveFile = new File(path + name + '/' + font + '.' + type);
        var saveOptions = new ExportOptionsSaveForWeb;
        // saveOptions.format = SaveDocumentType.PNG;
        saveOptions.format = type;
        app.activeDocument.saveAs(saveFile, saveOptions, true);
    }

    // let charList = new Array(94).fill(0).map((n, i) => String.fromCharCode(i+33));
    let charList = ["!","\"","#","$","%","&","'","(",")","*","+",",","-",".","/","0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","?","@","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","[","\\","]","^","_","`","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","{","|","}","~"];
    for(let i = 0; i < charList.length; i++){
        char = charList[i];
        layers[0].textItem.contents = char;
        saveAs((i+33).toString(), 'jpg');
    }

    alert('done');
}

generateTextImage('DejaVu Sans');