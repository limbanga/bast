# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'  # Hoặc SMTP của nhà cung cấp dịch vụ email
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@example.com'
# EMAIL_HOST_PASSWORD = 'your-email-password'
# DEFAULT_FROM_EMAIL = 'your-email@example.com'

CORS_ALLOW_ALL_ORIGINS=True
CSRF_TRUSTED_ORIGINS = [
  "https://g3wkj01v-r3g0p5xn-pabs4ggfvzcy.ac3-preview.marscode.dev"
]

print("Development settings loaded.")