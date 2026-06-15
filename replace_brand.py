import os
import re

dirs = ['/Users/zhangmingshan/open-webui/src', '/Users/zhangmingshan/open-webui/backend']

for d in dirs:
    for root, _, files in os.walk(d):
        for file in files:
            if file.endswith(('.svelte', '.ts', '.js', '.py', '.html')):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace variations of Open WebUI
                new_content = re.sub(r'(?i)open\s*webui', 'Lingrai', content)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f'Updated {filepath}')
