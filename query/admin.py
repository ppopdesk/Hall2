from django.contrib import admin

# Register your models here.
from .models import Query, QueryResponse

class QueryAdmin(admin.ModelAdmin):
    list_display = ["username","query_topic","date"]
    search_fields = ["username"]

admin.site.register(Query,QueryAdmin)
admin.site.register(QueryResponse)