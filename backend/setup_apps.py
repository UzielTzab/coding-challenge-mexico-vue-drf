import os

apps = ['health', 'exchanges', 'market_data', 'arbitrage', 'trading', 'wallets', 'system_logs']
base_dir = r'C:\Users\uzieltzab\Documents\ChallengeMexico\coding_challenge_mexico\backend\apps'

for app in apps:
    app_dir = os.path.join(base_dir, app)
    os.makedirs(app_dir, exist_ok=True)
    
    with open(os.path.join(app_dir, '__init__.py'), 'w') as f:
        f.write('')
        
    with open(os.path.join(app_dir, 'apps.py'), 'w') as f:
        f.write(f'''from django.apps import AppConfig

class {app.replace("_", " ").title().replace(" ", "")}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app}'
''')

    for filename in ['admin.py', 'models.py', 'views.py', 'urls.py', 'serializers.py']:
        filepath = os.path.join(app_dir, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                if filename == 'models.py':
                    f.write('from django.db import models\n\n')
                elif filename == 'admin.py':
                    f.write('from django.contrib import admin\n\n')
                else:
                    f.write('')
