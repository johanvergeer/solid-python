from python_solid_principles.jas.sales.entities import Sale


class SalesValidator:
    def validate(self, sale: Sale) -> None:
        if sale.total < 0:
            raise ValueError("A sale cannot have a total below 0.")
