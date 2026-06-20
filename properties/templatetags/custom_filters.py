from django import template

register = template.Library()

@register.filter
def indian_currency(value):
    try:
        value = float(value)

        if value >= 10000000:
            cr = value / 10000000
            return f"{cr:g} Cr"

        elif value >= 100000:
            lakh = value / 100000
            return f"{lakh:g} L"

        return f"{int(value):,}"

    except:
        return value