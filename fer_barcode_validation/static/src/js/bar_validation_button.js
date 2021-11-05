/** @odoo-module **/

import MainComponent from '@stock_barcode/components/main';
const rpc = require('web.rpc');
console.log("987654321");

// const rpc = require('web.rpc');

MainComponent.prototype._getProvider = async function(){ 
        var self = this;
        var id=self.props.id;
        return rpc.query({
            model: 'stock.picking',
            method: 'get_provider_cat',
            args: [id],
        }).then(function (res) {
            self.providerCategory = res;
        });
}

MainComponent.prototype.openProductPage = async function(){
    var provider = await this._getProvider();
    if(this.providerCategory=="Mayorista"){
        alert("No se pueden agregar nuevos productos a este pedido.")
    }
    else{
        if (!this._editedLineParams) {
            await this.env.model.save();
        }
        this.env.model.displayProductPage();
    }
}


