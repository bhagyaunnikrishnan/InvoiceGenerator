from flask import Flask, render_template, request, send_file
from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo, Item
from pyinvoice.templates import SimpleInvoice
import datetime, random

app = Flask(__name__)

@app.route('/')
def index():
    invoice_number = random.randint(1000,5000)
    return render_template('index.html',invoice_number = invoice_number)

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    if request.method == 'POST':

        # Get invoice details
        invoice_number = request.form['invoice_number']
        invoice_date = request.form['invoice_date']

        # Get service provider details
        provider_name = request.form['provider_name']
        provider_address = request.form['provider_address']
        provider_city = request.form['provider_city']
        provider_email = request.form['provider_email']

        # Get customer details
        customer_name = request.form['customer_name']
        customer_address = request.form['customer_address']
        customer_city = request.form['customer_city']
        customer_email = request.form['customer_email']

        doc = SimpleInvoice('invoice.pdf')

        now = datetime.datetime.now()

        doc.invoice_info = InvoiceInfo(invoice_number, now, invoice_date)
        doc.service_provider_info = ServiceProviderInfo(
            name= provider_name,
            street=provider_address,
            city=provider_city,
            
        )

        doc.client_info = ClientInfo(
            name = customer_name,
            street=customer_address,
            city=customer_city,
            email=customer_email
        )
         # Generate item details
        for key, value in request.form.items():
            if key.startswith('item_name_'):
                item_num = key.split('_')[-1]
                item_name = value
                unit = request.form[f"unit_{item_num}"]
                price = request.form[f"price_{item_num}"]
                doc.add_item(Item(item_name, item_name, unit, price))

        doc.set_item_tax_rate(request.form['tax_percentage'])
        doc.set_bottom_tip("Thankyou for shopping with us today! <br /> Please contact us at " + provider_email)
        doc.finish()

        
        # Send PDF as a downloadable file
        return send_file(
            'invoice.pdf',
            mimetype='application/pdf',
            as_attachment=False,
            download_name='generated_invoice.pdf'
        )
        
        
        





if __name__ == '__main__':
    app.run(debug = True)