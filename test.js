const _ = require('lodash');
const fs = require('fs');


let thuocBvtv = fs.readFileSync('./database_thuoc_bvtv.json');
thuocBvtv = JSON.parse(thuocBvtv);

for (var i in thuocBvtv) {
    for (var j in thuocBvtv[i].scopeOfUse) {
        if (thuocBvtv[i].scopeOfUse[j].plant == "lúa") {
            console.log(thuocBvtv[i].scopeOfUse[j].pest);
        }
    }
}