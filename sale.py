# This file is part of sale_description module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields

__all__ = ['SaleLine']
__metaclass__ = PoolMeta


class SaleLine:
    __name__ = 'sale.line'

    @fields.depends('product')
    def on_change_product(self):
        super(SaleLine, self).on_change_product()

        if self.product and self.product.description:
            self.description = self.product.description
