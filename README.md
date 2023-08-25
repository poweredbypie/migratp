# migratp
Migrates old 2.0 texture packs to 2.1.

# Usage
Install pillow:
```sh
pip install -r requirements.txt
```

Run:
```sh
python migrate.py $PACK_DIR $GD_RESOURCES_DIR
```

This will output the new translated game sheets in a new folder named `new`.
Use textureldr or replace the textures in the GD resources folder to apply the generated texture pack.