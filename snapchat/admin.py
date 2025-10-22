from django.contrib import admin
    
from .models import Chat

# admin.site.register(Chat)

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('emoji', 'name', 'time')   
    search_fields = ('name',)                  
    list_filter = ('time',)                    
    ordering = ('-id',)                        

try:
    admin.site.unregister(Chat)
except admin.sites.NotRegistered:
    pass

# ----------------------------
# Chat Admin
# ----------------------------
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('emoji', 'name', 'time')   # columns in admin
    search_fields = ('name',)
    ordering = ('-id',)

    # Customize permissions per user
    def get_model_perms(self, request):
        """
        Control access for different users:
        - Mahesh Babu (superuser) → full access
        - Saikrishna → view-only access
        """
        perms = super().get_model_perms(request)

        # Lowercase username to avoid case mismatch
        username = request.user.username.lower()

        if username == "saikrishna":

            perms['add'] = False
            perms['change'] = False
            perms['delete'] = False

        
        return perms