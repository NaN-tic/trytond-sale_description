=========================
Sale Description Scenario
=========================

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from operator import attrgetter
    >>> from proteus import config, Model, Wizard, Report
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts, create_tax
    >>> from.trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences, create_payment_term
    >>> today = datetime.date.today()

Create database::

    >>> config = config.set_trytond()
    >>> config.pool.test = True

Install sale::

    >>> Module = Model.get('ir.module')
    >>> sale_module, = Module.find([('name', '=', 'sale_description')])
    >>> sale_module.click('install')
    >>> Wizard('ir.module.install_upgrade').execute('upgrade')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Reload the context::

    >>> User = Model.get('res.user')
    >>> Group = Model.get('res.group')
    >>> config._context = User.get_preferences(True, config.context)

Translatable Lang::

    >>> Lang = Model.get('ir.lang')

    >>> lang_es, = Lang.find([('code', '=', 'es_ES')], limit=1)
    >>> lang_es.translatable = True
    >>> lang_es.save()

    >>> lang_ca, = Lang.find([('code', '=', 'ca_ES')], limit=1)
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

Create category::

    >>> ProductCategory = Model.get('product.category')
    >>> category = ProductCategory(name='Category')
    >>> category.save()

Create product::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> ProductTemplate = Model.get('product.template')
    >>> Product = Model.get('product.product')

    >>> config._context['language'] = 'es_ES'
    >>> product = Product()
    >>> template = ProductTemplate()
    >>> template.name = 'Product'
    >>> template.category = category
    >>> template.default_uom = unit
    >>> template.type = 'goods'
    >>> template.purchasable = True
    >>> template.salable = True
    >>> template.list_price = Decimal('10')
    >>> template.cost_price = Decimal('5')
    >>> template.cost_price_method = 'fixed'
    >>> template.account_expense = expense
    >>> template.account_revenue = revenue
    >>> template.customer_taxes.append(tax)
    >>> template.save()
    >>> product.template = template
    >>> product.description = 'Description es_ES'
    >>> product.save()

    >>> config._context['language'] = 'ca_ES'
    >>> product.description = 'Description ca_ES'
    >>> product.save()

Sale es_ES and ca_ES::

    >>> Sale = Model.get('sale.sale')
    >>> SaleLine = Model.get('sale.line')

    >>> sale_es = Sale()
    >>> sale_es.party = customer_es
    >>> sale_line_es = sale_es.lines.new()
    >>> sale_line_es.product = product
    >>> sale_line_es.description
    u'Description es_ES'

    >>> sale_ca = Sale()
    >>> sale_ca.party = customer_ca
    >>> sale_line_ca = sale_ca.lines.new()
    >>> sale_line_ca.product = product
    >>> sale_line_ca.description
    u'Description ca_ES'
