from django.db import models
from django.utils.text import slugify

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True # This tells Django not to create a table for this model


from django.db.models.functions import Lower

class Product(BaseModel):
    # ... previous fields ...

    class Meta:
        indexes = [
            # 1. Composite Index: Optimize filtering by category AND status simultaneously
            models.Index(fields=['category', 'is_active']),
            
            # 2. Functional Index: Optimize case-insensitive searches (PostgreSQL specific)
            models.Index(fields=['name'], name='product_name_idx'),
            models.Index(Lower('name'), name='product_name_lower_idx'),
        ]


git add apps/catalog/models.py apps/catalog/views.py core/settings.py
git commit -m "perf(database): implement query profiling and composite indexing" -m "Added Django Debug Toolbar for profiling, implemented PostgreSQL functional indexes, and optimized QuerySets with select_related."
git push origin main
