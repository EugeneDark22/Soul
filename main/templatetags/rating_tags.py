# rating_tags.py

from django import template

register = template.Library()

@register.filter(name='star_rating')
def star_rating(rating):
    """Відображає рейтинг як рядок з зірочками, включаючи половинні зірки."""
    if rating:
        full_stars = int(rating)
        half_star = int((rating - full_stars) * 2)  # Перевірка, чи є необхідність в половинній зірці
        empty_stars = 5 - full_stars - (1 if half_star else 0)
        return '★' * full_stars + ('½' if half_star else '') + '☆' * empty_stars
    return '☆' * 5  # Повертає 5 порожніх зірок, якщо рейтингу немає
