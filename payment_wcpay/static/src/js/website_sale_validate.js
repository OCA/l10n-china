$(document).ready(function () {

    var _poll_nbr = 0;

    function wcpay_payment_transaction_poll_status() {
        var order_node = $('div.oe_website_sale_tx_status');
        if (! order_node || order_node.data('orderId') === undefined &&
            order_node.data('invoiceId') === undefined) {
            return;
        }
        var order_id = order_node.data('orderId');
        var invoice_id = order_node.data('invoiceId');
        if (order_id) {
            return openerp.jsonRpc('/shop/payment/get_status_so/' + order_id, 'call', {
            }).then(function (result) {
                _poll_nbr += 1;
                if (result.recall && _poll_nbr <= 200) {
                    setTimeout(function () { wcpay_payment_transaction_poll_status(); }, 3000);
                }
                $('div.oe_website_sale_tx_status').html(result.message);
            });
        }
        else if(invoice_id) {
            return openerp.jsonRpc('/shop/payment/get_status_ai/' + invoice_id, 'call', {
            }).then(function (result) {
                _poll_nbr += 1;
                if (result.recall && _poll_nbr <= 200) {
                    setTimeout(function () { wcpay_payment_transaction_poll_status(); }, 3000);
                }
                $('div.oe_website_sale_tx_status').html(result.message);
            });
        }
    }

    wcpay_payment_transaction_poll_status();
});
