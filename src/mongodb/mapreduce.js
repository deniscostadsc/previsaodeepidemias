use previsaodeepidemias;

map = function (){
    var first;
    for (var disease in diseases){
        if (diseases[disease].test(this.text)){
            emit({
                disease: disease,
                week_start: firstDayOfWeek(this.created_at),
                location: this.location,
                location_str: this.location_str
            }, {
                count: 1
            });
        }
    }
};

reduce = function (key, emits){
    for (var i in emits){
        total += emits[i].count;
    }
    return {count: total};
};


db.raw_tweets.mapReduce(
    map,
    reduce,
    {
        keeptemp: true,
        out: 'disease_analysis',
        verbose: true,
        scope: {
            diseases: {
                'dengue': /dengue/i,
                'gripe': /h1n1|grip(e|ado|ada)/i,
                'tuberculose': /tuberculos[eoa]/i,
                'colera': /c[oó]lera/i,
                'malaria': /mal[aá]ria/i
            },

            firstDayOfWeek: function (date){
                var week = new Date(date.setDate(date.getDate() - date.getDay()));
                return new Date(week.getUTCFullYear(), week.getMonth() + 1, week.getDate());
            }
        }
    }
);
