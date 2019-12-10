const MongoClient = require('mongodb').MongoClient;
const url = "mongodb://localhost:27017/";
const fs = require('fs');
const _ = require('lodash');


function getDatabaseThuocBvtv() {
    let thuocBvtv = fs.readFileSync('./database_thuoc_bvtv.json');
    thuocBvtv = JSON.parse(thuocBvtv);
    return thuocBvtv;
}


class PlantProtectionProduct {
    constructor(db) {
        this.db = db;
    } 

    createRegistrationInfo(id, registrationInfo, cb = () => {}) {
        const collection = this.db.collection("registrationInfo");
    
        let obj = {
            pppId: id,
            registrationUnit: _.get(registrationInfo, "registrationUnit", ""),
            registrationUnitAddress: _.get(
                registrationInfo,
                "registrationUnitAddress",
                ""
            ),
            manufacturer: _.get(registrationInfo, "manufacturer", ""),
            manufacturerAddress: _.get(registrationInfo, "manufacturerAddress", ""),
            created: new Date()
        };
    
        // Save Registration Information
        collection.insertOne(obj, (err, res) => {
            if (err) {
                return cb(err, null);
            }
    
            const registrationInfo = res.ops[0];
    
            return cb(null, registrationInfo);
        });
    }


    createScopeOfUse(id, scopeOfUse, cb = () => {}) {
        const collection = this.db.collection("scopeOfUse");
    
        let obj = [];
        for (var i in scopeOfUse) {
            let data = {
            pppId: id,
            plant: _.get(scopeOfUse[i], "plant", ""),
            pest: _.get(scopeOfUse[i], "pest", ""),
            dosage: _.get(scopeOfUse[i], "dosage", ""),
            phi: _.get(scopeOfUse[i], "phi", ""),
            usage: _.get(scopeOfUse[i], "usage", ""),
            created: new Date()
            };
    
            obj.push(data);
        }
    
        // Save Scope Of Uses
        collection.insertMany(obj, (err, res) => {
            if (err) {
                return cb(err, null);
            }
            const scopeOfUse = res.ops;
            return cb(null, scopeOfUse);
        });
    }

    // CREATE NEW PLANT PROTECTION PRODUCT
    create(plantProtectionProduct = {}, cb = () => {}) {
        const collection = this.db.collection("plantProtectionProduct");
        var response = {};

        let pppObj = {
            name: _.get(plantProtectionProduct, "name", ""),
            activeIngredient: _.get(plantProtectionProduct, "activeIngredient", ""),
            content: _.get(plantProtectionProduct, "content", ""),
            plantProtectionProductsGroup: _.get(
            plantProtectionProduct,
            "plantProtectionProductGroup",
            ""
            ),
            ghs: _.get(plantProtectionProduct, "ghs", ""),
            who: _.get(plantProtectionProduct, "who", ""),
            created: new Date()
        };

        // Save plant protection product to database
        collection.insertOne(pppObj, (err, res) => {
            if (err) {
                return cb(err, null);
            }
            // Get plant protection product after created
            const pppId = res.insertedId;
            // Add plant protect product info to response
            response = res.ops[0];

            // Save scope of use to database
            const scopeOfUse = _.get(plantProtectionProduct, "scopeOfUse", []);

            this.createScopeOfUse(pppId, scopeOfUse, (err, scopeOfUse) => {
                if (err) {
                    return cb(err, null);
                }

                // Add scope of use to response
                response["scopeOfUse"] = scopeOfUse;
            });

            // Save registration info to database
            const registrationInfo = plantProtectionProduct.registrationInfo;

            this.createRegistrationInfo(
                pppId,
                registrationInfo,
                (err, registrationInfo) => {
                    if (err) {
                        return cb(err, null);
                    }

                    // Add registration info to response
                    response["registrationInfo"] = registrationInfo;

                    return cb(null, response);
                }
            );
        });
    }
}

MongoClient.connect(url, function(err, db) {
    if (err) throw err;
    var dbo = db.db("farm");

    const thuocBvtv = getDatabaseThuocBvtv();

    const plantProtectionProduct = new PlantProtectionProduct(dbo);

    let count = 0;
    for (var i in thuocBvtv) {
        plantProtectionProduct.create(thuocBvtv[i], (err, res) => {
            if (err) {
                console.log("Something wrong");
                return;
            }
            
            count++;

            console.log("Create thuoc bao ve thuc " + count);

            if (count == thuocBvtv.length) {
                console.log("Import thuoc bvtv successfully");
                db.close();
            }
        });
    }


    /////////////////////////////////////////////////////////////////////////////
    // TEST FOR FIRST 100 DOC 
    // var count = 0;
    // for (var i = 1; i <= 100; i++) {
    //     console.log("Import thuoc bvtv " + i);

    //     plantProtectionProduct.create(thuocBvtv[i], (err, res) => {
    //         count++;

    //         if (count == 100) {
    //             console.log("No lai la ok");
    //             db.close();
    //         }
    //     });
    // }
}); 

