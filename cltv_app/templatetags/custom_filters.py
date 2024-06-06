from django import template

register = template.Library()


@register.filter
def truncate_float(value, decimal_places=2):
    try:
        float_value = float(value)
        format_string = f"{{:.{decimal_places + 2}f}}"  # Format with extra precision
        formatted_value = format_string.format(float_value)
        integer_part, decimal_part = formatted_value.split(".")
        truncated_decimal_part = decimal_part[:decimal_places]
        return f"{integer_part}.{truncated_decimal_part}"
    except (ValueError, TypeError):
        return value


@register.filter
def split_string(value, separator=","):
    if not value or not isinstance(value, str):
        return value
    return value.split(separator)