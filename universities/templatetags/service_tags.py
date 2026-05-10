from django import template

register = template.Library()

@register.filter
def has_bus_service(university):
    """Check if university has bus service"""
    try:
        return university.busservice.has_bus_service
    except:
        return False

@register.filter
def has_hostel_service(university):
    """Check if university has hostel service"""
    try:
        return university.hostelservice.has_hostel_service
    except:
        return False

@register.filter
def has_playground_service(university):
    """Check if university has playground service"""
    try:
        return university.playgroundservice.has_playground_service
    except:
        return False
