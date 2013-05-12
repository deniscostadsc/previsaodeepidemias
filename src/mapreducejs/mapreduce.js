var diseases = ["dengue", "gripe", "tuberculose", "cólera", "doença de chagas", "malária"];
var diseases_re = [/dengue/i, /gripe/i, /tuberculose/i, /c[oó]lera/i, /doen[cç]a de chagas/i, /mal[aá]ria/i];

var map = function(text){
    for (var i=0; disease_re.length; i++) {
        if (disease_re.exec(text))
            return {}
    };

