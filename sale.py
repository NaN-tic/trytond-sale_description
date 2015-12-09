# This file is part of sale_description module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.transaction import Transaction

__all__ = ['SaleLine']
__metaclass__ = PoolMeta


class SaleLine:
    __name__ = 'sale.line'

    @fields.depends('product')
    def on_change_product(self):
        Product = Pool().get('product.product')

        super(SaleLine, self).on_change_product()

        lang = Transaction().context.get('language')

        if self.product and self.product.description:
            # get party lang
            party_context = {}
            if self.sale and self.sale.party:
                party = self.sale.party
                if party.lang:
                    party_context['language'] = party.lang.code

            # reload product by lang when is different party lang and user lang
            if party_context.get('language') and (lang != party_context['language']):
                with Transaction().set_context(party_context):
                    self.description = Product(self.product.id).description
            else:
                self.description = self.product.description
