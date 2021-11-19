odoo.define('pos_mrp_order.models_mrp_order', function (require) {
    "use strict";
    console.log('Dentro de MRP_POS_ORDER')
    const models = require('point_of_sale.models');
    const { parse } = require('web.field_utils');
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const { onChangeOrder } = require('point_of_sale.custom_hooks');
    const { useListener } = require('web.custom_hooks');
    const { useErrorHandlers } = require('point_of_sale.custom_hooks');
    const rpc = require('web.rpc');
    
    const _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        load_server_data(){
            const len = this.models.length
            for (let i=0; i <= len; i++){
                if (this.models[i] !== undefined && this.models[i].model === 'product.product'){
                    this.models[i].fields.push('to_make_mrp')
                }
            }
            let result = _super_posmodel.load_server_data.apply(this, arguments);
            // console.log(this.models)
            return result;
        }
    });

    const MrpPaymentScreen = PaymentScreen => class extends PaymentScreen {
        constructor() {
            super(...arguments);
        }
        async validateOrder(isForceValidate) {
            await this.send_mrp(); // agregada
            await super.validateOrder(...arguments);
        }
        
        async send_mrp(){
            let orderlines = this.currentOrder.orderlines
            let lines = orderlines.models
            let len = lines.length
            console.log(this.currentOrder)
            const list_product = []
            for (let i=0; i < len; i++){
                if (lines[i].product.to_make_mrp){
                    if (lines[i].quantity > 0) {
                        let product_dict = {
                            'id': lines[i].product.id,
                            'qty': lines[i].quantity,
                            'product_tmpl_id': lines[i].product.product_tmpl_id,
                            'pos_reference': this.currentOrder.name,
                            'uom_id': lines[i].product.uom_id[0],
                        };
                        list_product.push(product_dict);
                    }
                }
            }
            if (list_product.length) {
                rpc.query({
                    model: 'mrp.production',
                    method: 'create_mrp_from_pos',
                    args: [1, list_product],
                });
            }
        }
    }
    // PaymentScreen.template = 'PaymentScreen';

    // Registries.Component.add(PaymentScreen);
    Registries.Component.extend(PaymentScreen, MrpPaymentScreen)

    return MrpPaymentScreen;
});
