pip install -U pip
pip install -U g4f~=0.2.0.3

mkdir -p ./tmp
if [ -n "$PROMPT" ]; then
    python prompt.py $CONFIGPATH "$PROMPT"
else 
    python prompt.py $CONFIGPATH
fi