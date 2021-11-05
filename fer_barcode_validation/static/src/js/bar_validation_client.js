/** @odoo-module **/

import ViewsWidget from '@stock_barcode/widgets/views_widget';


ViewsWidget.include({

    /**
     * Handles the click on the `confirm button`.
     *
     * @private
     * @param {MouseEvent} ev
     */
    _onClickSave: async function (ev) {
        ev.stopPropagation();
        console.log("2");
        var self = this;
        console.dir(self);
        var record1 = self.controller.model.get(self.controller.handle);
        console.dir(record1.data.picking_id.res_id);
        var qty_done=record1.data.qty_done;
        var qty_total=record1.data.product_uom_qty;
        console.dir(record1);
        console.dir(record1.data);
        var provider = await this._getProvider(record1.data.picking_id.res_id);
        console.log(this.providerCategory);

        if(this.providerCategory=="Mayorista"){
            if(qty_done > qty_total){
                alert("No se puede asignar una cantidad mayor a la pedida.")
            }
            else{
                await this.controller.saveRecord(this.controller.handle, {
                    stayInEdit: true,
                    reload: false,
                });
                const record = this.controller.model.get(this.controller.handle);
                this.trigger_up('refresh', { recordId: record.res_id });
                }
        }
        else{
            await this.controller.saveRecord(this.controller.handle, {
                stayInEdit: true,
                reload: false,
            });
            const record = this.controller.model.get(this.controller.handle);
            this.trigger_up('refresh', { recordId: record.res_id });
            }
    },

    _getProvider: function (id) {
        var self = this;
        // console.dir(self.actionParams.id);
        return this._rpc({
            model: 'stock.picking',
            method: 'get_provider_cat',
            args: [id],
        }).then(function (res) {
            self.providerCategory = res;
        });
    },
});

export default ViewsWidget;
