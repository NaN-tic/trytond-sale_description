=========================
Sale Description Scenario
=========================

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from operator import attrgetter
    >>> from proteus import config, Model, Wizard, Report
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts, create_tax
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences, create_payment_term
    >>> today = datetime.date.today()

Install sale_description::

    >>> config = activate_modules('sale_description')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Translatable Lang::

    >>> Lang = Model.get('ir.lang')

    >>> lang_es, = Lang.find([('code', '=', 'es')], limit=1)
    >>> lang_es.translatable = True
    >>> lang_es.save()

    >>> lang_ca, = Lang.find([('code', '=', 'ca')], limit=1)
    >>> lang_ca.translatable = True
    >>> lang_ca.save()

Create fiscal year::

    >>> fiscalyear = set_fiscalyear_invoice_sequences(
    ...     create_fiscalyear(company))
    >>> fiscalyear.click('create_period')

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> revenue = accounts['revenue']
    >>> expense = accounts['expense']
    >>> cash = accounts['cash']

    >>> Journal = Model.get('account.journal')
    >>> cash_journal, = Journal.find([('type', '=', 'cash')])
    >>> cash_journal.credit_account = cash
    >>> cash_journal.debit_account = cash
    >>> cash_journal.save()

Create tax::

    >>> tax = create_tax(Decimal('.10'))
    >>> tax.save()

Create parties::

    >>> Party = Model.get('party.party')

    >>> customer_es = Party()
    >>> customer_es.name = 'Customer ES'
    >>> customer_es.lang = lang_es
    >>> customer_es.save()

    >>> customer_ca = Party()
    >>> customer_ca.name = 'Customer CA'
    >>> customer_ca.lang = lang_ca
    >>> customer_ca.save()

Create account categories::

    >>> ProductCategory = Model.get('product.category')
    >>> account_category = ProductCategory(name="Account Category")
    >>> account_category.accounting = True
    >>> account_category.account_expense = expense
    >>> account_category.account_revenue = revenue
    >>> account_category.save()

    >>> account_category_tax, = account_category.duplicate()
    >>> account_category_tax.customer_taxes.append(tax)
    >>> account_category_tax.save()

Create product::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> ProductTemplate = Model.get('product.template')
    >>> Product = Model.get('product.product')

    >>> config._context['language'] = 'es'
    >>> product = Product()
    >>> template = ProductTemplate()
    >>> template.name = 'Product'
    >>> template.default_uom = unit
    >>> template.type = 'goods'
    >>> template.purchasable = True
    >>> template.salable = True
    >>> template.list_price = Decimal('10')
    >>> template.cost_price = Decimal('5')
    >>> template.cost_price_method = 'fixed'
    >>> template.account_category = account_category_tax
    >>> template.save()
    >>> product, = template.products
    >>> product.description = 'Description es_ES'
    >>> product.save()

    >>> config._context['language'] = 'ca'
    >>> product.description = 'Description ca_ES'
    >>> product.save()

Sale es and ca::

    >>> Sale = Model.get('sale.sale')
    >>> SaleLine = Model.get('sale.line')

    >>> sale_es = Sale()
    >>> sale_es.party = customer_es
    >>> sale_line_es = sale_es.lines.new()
    >>> sale_line_es.product = product
    >>> sale_line_es.description
    'Description es_ES'

    >>> sale_ca = Sale()
    >>> sale_ca.party = customer_ca
    >>> sale_line_ca = sale_ca.lines.new()
    >>> sale_line_ca.product = product
    >>> sale_line_ca.description
    'Description ca_ES'
