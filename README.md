# migratp
Migrates old 2.0 texture packs to 2.1.

# Usage
Install pillow:
```sh
pip install -r requirements.txt
```

Run:
```sh
python migrate.py $PACK_DIR $GD_RESOURCES_DIR $OUT_DIR
```

This will output the new translated game sheets in the new folder specified (`$OUT_DIR`)
Use textureldr or replace the textures in the GD resources folder to apply the generated texture pack.