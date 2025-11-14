from django.contrib import admin
from django.utils.html import format_html
from .models import Room, Message
from .encryption import decrypt_message

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at', 'password_status')
    list_filter = ('created_at',)
    search_fields = ('name', 'created_by__username')
    readonly_fields = ('created_at',)
    
    def password_status(self, obj):
        return format_html(
            '<span style="color: green; font-weight: bold;">🔒 Protected</span>'
        )
    password_status.short_description = 'Password Status'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'room', 'encryption_status', 'decrypted_preview', 'timestamp')
    list_filter = ('room', 'timestamp')
    search_fields = ('sender__username', 'room__name')
    readonly_fields = ('timestamp', 'encrypted_content', 'decrypted_content_display')
    
    fieldsets = (
        ('Message Info', {
            'fields': ('room', 'sender', 'timestamp')
        }),
        ('Encryption Details', {
            'fields': ('encrypted_content', 'decrypted_content_display'),
            'description': 'Messages are encrypted using Fernet (AES-128) symmetric encryption'
        }),
    )
    
    def encryption_status(self, obj):
        return format_html(
            '<span style="color: green; font-weight: bold;">🔐 ENCRYPTED</span>'
        )
    encryption_status.short_description = 'Encryption Status'
    
    def decrypted_preview(self, obj):
        try:
            decrypted = decrypt_message(obj.encrypted_content)
            preview = decrypted[:50] + '...' if len(decrypted) > 50 else decrypted
            return preview
        except:
            return '[Decryption Error]'
    decrypted_preview.short_description = 'Message Preview'
    
    def decrypted_content_display(self, obj):
        try:
            decrypted = decrypt_message(obj.encrypted_content)
            return format_html(
                '<div style="padding: 10px; background: #f0f0f0; border-radius: 5px;">{}</div>',
                decrypted
            )
        except:
            return format_html(
                '<span style="color: red;">Unable to decrypt message</span>'
            )
    decrypted_content_display.short_description = 'Decrypted Content'
