from pathlib import Path

p = Path("C:/Users/ghhrr/OneDrive/Bureau")
print(p.name)

for i in p.iterdir():
    print(i)